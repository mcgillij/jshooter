from cx_Freeze import setup, Executable

setup(
    name="jshooter",
    version="0.1",
    description="shooting game test",
    executables=[Executable("jshooter.py")],
)
