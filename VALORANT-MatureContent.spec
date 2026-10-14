# Build both executables:  pyinstaller VALORANT-MatureContent.spec
# Output goes to dist/. The data folder is bundled, but a data folder placed
# next to the .exe takes priority, so new patch files can be dropped in without a rebuild.

datas = [('data/MatureData-WindowsClient.*', 'data'), ('logo/vlr.png', 'logo')]

gui = Analysis(['app.py'], datas=datas)
gui_exe = EXE(
    PYZ(gui.pure),
    gui.scripts, gui.binaries, gui.datas,
    name='VALORANT-MatureContent-Manager',
    icon='logo/vlr.ico',
    console=False,
)

cli = Analysis(['cli.py'], datas=datas)
cli_exe = EXE(
    PYZ(cli.pure),
    cli.scripts, cli.binaries, cli.datas,
    name='VALORANT-MatureContent-CLI',
    icon='logo/vlr.ico',
    console=True,
)
