'''

Copyright (C) 2017-2019 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from scif.logger import bot
import sys
import pwd
import os


def main(args,parser,subparser):

    from scif.main import ScifRecipe
    apps = args.recipe

    if len(apps) > 0:
        recipe = apps.pop(0)

        if not os.path.exists(recipe):
            bot.exit("Cannot find recipe file %s" %recipe)

        client = ScifRecipe(recipe, writable=False)

        # Preview the entire recipe, or the apps chosen
        client.preview(apps)

    else:
        bot.info('You must provide a recipe file to preview!')
