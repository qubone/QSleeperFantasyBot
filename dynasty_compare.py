from fantasycalc import get_player_value
async def dynasty_compare(side_a: list, side_b: list):
    async def total_value(assets):
        total = 0
        asset_details = []
        for name in assets:
            player = await get_player_value(name, is_dynasty=True)
            if player:
                value = player.value
                total += value
                asset_details.append((player.info.name, value))
            else:
                asset_details.append((name, 0))
        return total, asset_details

    total_a, details_a = await total_value(side_a)
    total_b, details_b = await total_value(side_b)

    advantage = "Side A" if total_a > total_b else "Side B"
    diff = abs(total_a - total_b)

    def format_side(details):
        return "\n".join([f"  - {name}: {val}" for name, val in details])

    result = (
        f"🔁 Dynasty Trade Comparison\n\n"
        f"🅰️ Side A Total: {total_a}\n{format_side(details_a)}\n\n"
        f"🅱️ Side B Total: {total_b}\n{format_side(details_b)}\n\n"
        f"➡️ **Advantage:** {advantage} by {diff} points"
    )

    return result