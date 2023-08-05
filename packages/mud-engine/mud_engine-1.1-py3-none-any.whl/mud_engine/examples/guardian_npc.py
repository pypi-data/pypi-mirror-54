from mud_engine.npc import NPC
from mud_engine.geography import Geography
from mud_engine.game import Game
from mud_engine.geography import GeographyFactory
from mud_engine.help import Help
from mud_engine.base import MUDMessage

class GuardianNPC(NPC):

    directions_protected = None

    def __init__(self, *args, **kwargs):
        self.directions_protected = kwargs.get("directions_protected", [])
        super().__init__(*args, **kwargs)

    def queue_message(self, message, *args, **kwargs):

        context = getattr(message, 'context', None)

        if not context or 'command' not in context or 'player' not in context:
            return

        self.handle_command(f"tell {context['player'].name} leave me a lone.")

class GuardedGeography(Geography):

    def move_player(self, player, direction):
        # Are there any guardians in the room?
        for guardian_player in self.players:
            if isinstance(guardian_player, GuardianNPC):
                if direction in guardian_player.directions_protected:
                    player.message_location(f"{guardian_player.name} shoves you back, exclaiming 'You shall not pass!'",
                        f"{guardian_player.name} shoves {player.name}, exclaiming 'You shall not pass!'")
                    return

        super().move_player(player, direction)

class GuardianMUD(Game):

    name = "Guardian MUD"

    async def run(self):

        from mud_engine.communication import Brown
        from mud_engine.communication import NoColor
        from mud_engine.help import HelpInterface

        orig_default_help = HelpInterface.default_help

        # Let's update the default help behavior to include some Guardian MUD details AND do the default display
        def new_default_help(self):
            msg = "Guardian MUD is now up and running!\r\n\r\n"
            return msg + orig_default_help(self)

        HelpInterface.default_help = new_default_help

        Help("guardian", "Guardian is a mud about trying to get past a guardian!")

        # Lets override the default geography
        starting_geo = GeographyFactory.create_geography(
            0,
            0,
            0,
            "A country road",
            "You stand on a winding country road, dividing a grassy field",
        )
        bridge_ent_geo = GeographyFactory.create_geography(
            *starting_geo.get_direction_coordinates("north"),
            "The bridge entrance",
            "You've come to the end of a country road. Up ahead there's a sign and bridge crossing a river",
            entrance_descriptions={
                "north": "A bridge crossing a river",
            }
        )

        bridge_geo = GeographyFactory.create_geography(
            *bridge_ent_geo.get_direction_coordinates("north"),
            "A rickety wooden bridge",
            "You stand on a bridge that doesn't inspire much confidence in it's sturdyness",
            npcs=[
                GuardianNPC(
                    name="Bridge Troll",
                    directions_protected=["north"]
                )
            ],
            type="guardedgeography"
        )

        return await super().run()


if __name__ == "__main__":

    import sys
    import os
    import logging
    import asyncio

    logging.basicConfig(level=logging.DEBUG)
    host = "127.0.0.1" if not (len(sys.argv) > 2 and sys.argv[1]) else sys.argv[1]
    port = 5000 if not (len(sys.argv) > 2 and sys.argv[2]) else sys.argv[2]
    mud = GuardianMUD(host, int(port))
    mud.admins.append(os.environ.get('ADMIN', 'ben'))
    asyncio.run(mud.run())
    sys.exit(0)
