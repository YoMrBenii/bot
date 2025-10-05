import discord
from discord.ext import commands
from mongo import *  # expects `db` and your helpers
from functions import owneronly
import logging, traceback

# ---- logging setup (simple, non-duplicating) ----
logger = logging.getLogger("cog.wallet")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.DEBUG)


def _coerce_num(x):
    """Return a numeric value, or 0 if x is None/invalid."""
    if x is None:
        return 0
    if isinstance(x, (int, float)):
        return x
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0


def _safe_getuservar(var: str, userid: str | int):
    """getuservar that never raises and never returns None/str."""
    try:
        val = getuservar(var, str(userid))
        val = _coerce_num(val)
        logger.debug("[wallet] getuservar(%s, %s) -> %s", var, userid, val)
        return val
    except Exception:
        logger.exception("[wallet] getuservar crashed for var=%r user=%r", var, userid)
        return 0


def _safe_getlbspot(var: str, userid: str | int):
    """
    Calls getlbspot but shields KeyError (e.g., documents missing 'usd').
    Returns an int rank or None if unavailable.
    """
    try:
        r = getlbspot(var, str(userid))
        # Normalize result
        if isinstance(r, int) and r > 0:
            return r
        return None
    except KeyError as e:
        # This is the 'usd' KeyError you saw; log and degrade gracefully.
        logger.exception("[wallet] KeyError inside getlbspot(%r, %r): missing key %r", var, userid, e.args[0] if e.args else None)
        return None
    except Exception:
        logger.exception("[wallet] getlbspot crashed for var=%r user=%r", var, userid)
        return None


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wallet(self, ctx, member: discord.Member = None):
        try:
            # --- Resolve member ---
            try:
                if member is None:
                    member = ctx.author
                memberid = str(member.id)
                memname = member.name
                logger.debug("[wallet] member resolved: id=%s name=%s", memberid, memname)
            except Exception:
                logger.exception("[wallet] member resolution failed")
                await ctx.send("❌ Member resolution failed.")
                return

            # --- Read values safely ---
            money = _safe_getuservar("usd", memberid)
            permlvl = _safe_getuservar("permlvl", memberid)
            rep_val = _safe_getuservar("rep", memberid)

            # Leaderboard can be the culprit: guard it explicitly
            try:
                lb_val = _safe_getlbspot("usd", memberid)
                lbspot = f"\nRank: {lb_val}" if lb_val else ""
            except Exception:
                logger.exception("[wallet] lbspot formatting failed")
                lbspot = ""

            permtext = f"\nPermlvl: {int(permlvl)}" if _coerce_num(permlvl) > 0 else ""
            reptext = f"\nRep: {int(_coerce_num(rep_val))}"

            # --- Build embed ---
            try:
                money_num = _coerce_num(money)
                desc = f"<@{memberid}> has {round(money_num):,} dollars.{lbspot}{reptext}{permtext}"
                embed = discord.Embed(
                    description=desc,
                    title=f"{memname}'s wallet",
                    colour=0x000000
                )
            except Exception:
                logger.exception("[wallet] embed construction failed")
                await ctx.send("❌ Failed to build the wallet embed.")
                return

            # --- Send ---
            await ctx.send(embed=embed)

        except Exception as e:
            # Final safety net: show type and message to the user; full traceback to console
            await ctx.send(f"❌ {type(e).__name__}: `{e}`")
            logger.error("[wallet] Unhandled exception\n%s", traceback.format_exc())

    @commands.command()
    async def em(self, ctx):
        if owneronly(ctx.author) is False:
            return await ctx.send("Owner only")
        try:
            userid = str(ctx.author.id)
            # Make sure your writer has upsert=True internally
            setuservar("usd", userid, 5)
            await ctx.send("Added 5 USD to your wallet.")
        except Exception as e:
            await ctx.send(f"❌ {type(e).__name__}: `{e}`")
            logger.error("[wallet.em] Exception\n%s", traceback.format_exc())

    # Optional: maintenance command to normalize DB. Owner-only.
    @commands.command()
    async def fixusd(self, ctx):
        if owneronly(ctx.author) is False:
            return await ctx.send("Owner only")
        try:
            # Normalize: any missing or null usd -> 0
            r1 = db.users.update_many({"usd": {"$exists": False}}, {"$set": {"usd": 0}})
            r2 = db.users.update_many({"usd": None}, {"$set": {"usd": 0}})
            await ctx.send(f"Patched docs: set usd=0 on {(r1.modified_count or 0) + (r2.modified_count or 0)} users.")
        except Exception as e:
            await ctx.send(f"❌ {type(e).__name__}: `{e}`")
            logger.error("[wallet.fixusd] Exception\n%s", traceback.format_exc())


async def setup(bot):
    await bot.add_cog(Wallet(bot))

