import click


class AliasedGroup(click.Group):
    """
    A class for a group able to match subcommands even if only a substring is matched

    Examples:
        bot wh -> bot whoami (because there is no other command starting with `wh`)
    """

    def get_command(self, ctx, cmd_name):
        """
        Override get_command to return commands if matching a unique substring (es. rapp for rapportini)
        Args:
            ctx ():
            cmd_name ():

        Returns:
            the command that matched if it is unique, a fail if it is not unique, None if no command matches
        """
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return super().get_command(ctx, matches[0])
        else:
            ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))
