# ChecksMate Chess Randomizer Setup Guide

![A chess piece with several blurry opposing pieces in the background](https://i.imgur.com/fqng206.png)

## Required Software

- Any ChecksMate client. Currently, a modified ChessV client is supported and can be accessed via
  its [Github releases Page](https://github.com/chesslogic/chessv/releases) (latest version)
- Archipelago from the [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    - (select `ChecksMate Client` during installation.)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

Some releases of the ChecksMate client include an example YAML file demonstrating some supported options.

### Where do I get a YAML file?

You can customize your settings by visiting the [ChecksMate Player Settings Page](/games/ChecksMate/player-settings)

#### Warning: Locations Accessibility not supported

It is strongly recommended that you **do not use *Accessibility: Locations***. Most testing is at *Minimal*, although
*Items* should also function. (Generation will often fail. The custom item pool generation does not guarantee that you
will receive the combinations the logic believes necessary to access every location. Once location distribution begins,
there is no way to revisit item pool generation.)

#### Opinion: Material Balancing

One of the most important settings determines how many pieces will be distributed through your multiworld, defined in
terms of material value. Although your multiworld's item pool may contain more than 39 material, you should not expect
to have all of your material before reaching your goal: The logic requires that you equal the CPU army, not that you
complete your collection.

A normal (FIDE) army has 8 points of pawns plus 31 points of pieces (12 from 4 minor pieces, 10 from 2 rooks, and 9 from
1 queen). Material isn't everything: An army of 27 pawns plus 4 Knights is considered to be extremely powerful.
Conversely, having no pawns whatsoever opens your position dramatically, allowing your pieces to make very aggressive
moves and to maintain a very high tempo.

### Generating a ChecksMate game

**ChecksMate is a short game! You might restart many times, but you should expect no more than an hour of gameplay!**

When you join a multiworld game, you will be asked to provide your YAML file to whoever is hosting. Once that is done,
the host will provide you with either a link to download your data file, or with a zip file containing everyone's data
files. You do not have a file inside that zip though!

You need to start a ChecksMate client yourself, which are available from the Releases page (see above). Generally, these
need to be extracted to a folder before they are run, due to dependency on asset files and dynamic libraries.

### Connect to the MultiServer

First start ChecksMate.

Once ChecksMate is started. In the client at the top type in the spot labeled `Server` type the `Ip Address` and `Port`
separated with a `:` symbol. Then input your slot name in the next box. The third box can be used for any password,
which is often left empty.

These connection settings will be saved in a simple text file for the next time you start the client. (You may safely
delete this convenience file.)

### Play the game

When the console tells you that you have joined the room, you're all set. Congratulations on successfully joining a
multiworld game!
