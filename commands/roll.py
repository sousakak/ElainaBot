import random

async def roll(ctx, dice):
  """Rolls a dice in N,N format."""
  try:
    rolls, limit = map(int, dice.split(','))
  except Exception:
    async with ctx.channel.typing():
      await ctx.response.send_message(
        '2つの数字をカンマで区切ってくださいね。あれ、もしかしてやり方わかんないんですか？')
    return

  result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
  async with ctx.channel.typing():
    await ctx.response.send_message(result)