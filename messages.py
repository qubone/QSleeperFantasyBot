from player_model import Player

def construct_trade_message(player_a: Player, player_b: Player) -> str:
    """
    Constructs a trade evaluation message for Discord.

    Args:
        player_a (Player): Model of Player A.
        player_b (Player): Model of Player B.

    Returns:
        str: Formatted trade evaluation message.
    """
    return (
        f"🔄 **Trade Evaluation**\n"
        f"**{player_a.info.name}**: {player_a.value} pts\n"
        f"**{player_b.info.name}**: {player_b.value} pts\n\n"
        f"{player_a.info.name} {'>' if player_a.value > player_b.value else '<'} {player_b.info.name}"
    )