"""
  Test for the "apio build" command
"""

# -- apio build entry point
from apio.commands.build import cli as cmd_build


# pylint: disable=too-many-statements
def test_errors_without_apio_ini_1(click_cmd_runner, setup_apio_test_env):
    """Test: Various errors 1/2. All tests are without apio.ini and without
    apio packages installed."""

    with click_cmd_runner.isolated_filesystem():

        # -- Config the apio test environment
        setup_apio_test_env()

        # -- Execute "apio build"
        result = click_cmd_runner.invoke(cmd_build)
        assert result.exit_code != 0, result.output
        assert "Info: Project has no apio.ini file" in result.output
        assert "Error: insufficient arguments: missing board" in result.output
        assert "Error: Missing FPGA" in result.output

        # apio build --board icestick
        result = click_cmd_runner.invoke(cmd_build, ["--board", "icestick"])
        assert result.exit_code == 1, result.output
        assert "apio packages --install --force oss-cad-suite" in result.output

        # apio build --fpga iCE40-HX1K-VQ100
        result = click_cmd_runner.invoke(
            cmd_build, ["--fpga", "iCE40-HX1K-VQ100"]
        )
        assert result.exit_code == 1, result.output
        assert "apio packages --install --force oss-cad-suite" in result.output

        # apio build --type lp --size 8k --pack cm225:4k
        result = click_cmd_runner.invoke(
            cmd_build, ["--type", "lp", "--size", "8k", "--pack", "cm225:4k"]
        )
        assert result.exit_code == 1, result.output
        assert "Error: insufficient arguments" in result.output

        # apio build --board icezum --size 1k
        result = click_cmd_runner.invoke(
            cmd_build, ["--board", "icezum", "--size", "1k"]
        )
        assert result.exit_code != 0, result.output
        assert "apio packages --install --force oss-cad-suite" in result.output

        # apio build --board icezum --fpga iCE40-HX1K-TQ144 --type hx
        result = click_cmd_runner.invoke(
            cmd_build,
            [
                "--board",
                "icezum",
                "--fpga",
                "iCE40-HX1K-TQ144",
                "--type",
                "hx",
            ],
        )
        assert result.exit_code != 0, result.output
        assert "apio packages --install --force oss-cad-suite" in result.output

        # apio build --board icezum --pack tq144
        result = click_cmd_runner.invoke(
            cmd_build, ["--board", "icezum", "--pack", "tq144"]
        )
        assert result.exit_code != 0, result.output
        assert "apio packages --install --force oss-cad-suite" in result.output

        # apio build --fpga iCE40-HX1K-TQ144 --pack tq144 --size 1k
        result = click_cmd_runner.invoke(
            cmd_build,
            ["--fpga", "iCE40-HX1K-TQ144", "--pack", "tq144", "--size", "1k"],
        )
        assert result.exit_code != 0, result.output
        assert "apio packages --install --force oss-cad-suite" in result.output

        # apio build --fpga iCE40-HX1K-TQ144 --type hx
        result = click_cmd_runner.invoke(
            cmd_build, ["--fpga", "iCE40-HX1K-TQ144", "--type", "hx"]
        )
        assert result.exit_code != 0, result.output
        assert "apio packages --install --force oss-cad-suite" in result.output

        # apio build --board icezum --size 8k
        result = click_cmd_runner.invoke(
            cmd_build, ["--board", "icezum", "--size", "8k"]
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'size' = (1k vs 8k)"
            in result.output
        )

        # apio build --board icezum --fpga iCE40-HX1K-TQ144 --type lp
        result = click_cmd_runner.invoke(
            cmd_build,
            [
                "--board",
                "icezum",
                "--fpga",
                "iCE40-HX1K-TQ144",
                "--type",
                "lp",
            ],
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'type' = (hx vs lp)"
            in result.output
        )

        # apio build --board icezum --fpga iCE40-HX1K-VQ100
        result = click_cmd_runner.invoke(
            cmd_build, ["--board", "icezum", "--fpga", "iCE40-HX1K-VQ100"]
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'fpga' = "
            "(iCE40-HX1K-TQ144 vs iCE40-HX1K-VQ100)" in result.output
        )

        # apio build --fpga iCE40-HX1K-TQ144 --type lp --size 8k
        result = click_cmd_runner.invoke(
            cmd_build,
            ["--fpga", "iCE40-HX1K-TQ144", "--type", "lp", "--size", "8k"],
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'type' = (hx vs lp)"
            in result.output
        )

        # apio build --fpga iCE40-HX1K-TQ144 --pack vq100
        result = click_cmd_runner.invoke(
            cmd_build, ["--fpga", "iCE40-HX1K-TQ144", "--pack", "vq100"]
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'pack' = (tq144 vs vq100)"
            in result.output
        )

        # apio build --board icezum --pack vq100
        result = click_cmd_runner.invoke(
            cmd_build, ["--board", "icezum", "--pack", "vq100"]
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'pack' = (tq144 vs vq100)"
            in result.output
        )

        # apio build --size 8k
        result = click_cmd_runner.invoke(cmd_build, ["--size", "8k"])
        assert result.exit_code != 0, result.output
        assert "Error: insufficient arguments" in result.output


def test_errors_without_apio_ini_2(click_cmd_runner, setup_apio_test_env):
    """Test: Various errors 2/2. All tests are without apio.ini and without
    apio packages installed."""
    with click_cmd_runner.isolated_filesystem():

        # -- Config the apio test environment
        setup_apio_test_env()

        # apio build --type lp
        result = click_cmd_runner.invoke(cmd_build, ["--type", "lp"])
        assert result.exit_code != 0, result.output
        assert "Error: insufficient arguments" in result.output

        # apio build --type lp --size 8k
        result = click_cmd_runner.invoke(
            cmd_build, ["--type", "lp", "--size", "8k"]
        )
        assert result.exit_code != 0, result.output
        assert "Error: insufficient arguments" in result.output

        # apio build --board icefake
        result = click_cmd_runner.invoke(cmd_build, ["--board", "icefake"])
        assert result.exit_code != 0, result.output
        assert "Error: unknown board: icefake" in result.output

        # apio build --board icefake --fpga iCE40-HX1K-TQ144
        result = click_cmd_runner.invoke(
            cmd_build, ["--board", "icefake", "--fpga", "iCE40-HX1K-TQ144"]
        )
        assert result.exit_code != 0, result.output
        assert "Error: unknown board: icefake" in result.output

        # apio build --fpga iCE40-FAKE
        result = click_cmd_runner.invoke(cmd_build, ["--fpga", "iCE40-FAKE"])
        assert result.exit_code != 0, result.output
        assert "Error: unknown FPGA: iCE40-FAKE" in result.output

        # apio build --fpga iCE40-FAKE --size 8k
        result = click_cmd_runner.invoke(
            cmd_build, ["--fpga", "iCE40-FAKE", "--size", "8k"]
        )
        assert result.exit_code != 0, result.output
        assert "Error: unknown FPGA: iCE40-FAKE" in result.output

        # apio build --board icezum --fpga iCE40-FAKE
        result = click_cmd_runner.invoke(
            cmd_build, ["--board", "icezum", "--fpga", "iCE40-FAKE"]
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'fpga' = "
            "(iCE40-HX1K-TQ144 vs iCE40-FAKE)" in result.output
        )


def test_errors_with_apio_ini(
    click_cmd_runner, setup_apio_test_env, write_apio_ini
):
    """Test: apio build with apio create"""

    with click_cmd_runner.isolated_filesystem():

        # -- Config the apio test environment
        setup_apio_test_env()

        # -- Write apio.ini
        write_apio_ini({"board": "icezum", "top-module": "main"})

        # apio build
        result = click_cmd_runner.invoke(cmd_build)
        assert result.exit_code != 0, result.output

        # apio build --board icestick
        result = click_cmd_runner.invoke(cmd_build, ["--board", "icestick"])
        assert result.exit_code != 0, result.output
        assert (
            "Info: ignoring board specification from apio.ini."
            in result.output
        )

        # apio build --fpga iCE40-HX1K-VQ100
        result = click_cmd_runner.invoke(
            cmd_build, ["--fpga", "iCE40-HX1K-VQ100"]
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'fpga' = "
            "(iCE40-HX1K-TQ144 vs iCE40-HX1K-VQ100)" in result.output
        )

        # apio build --type lp --size 8k --pack cm225:4k
        result = click_cmd_runner.invoke(
            cmd_build, ["--type", "lp", "--size", "8k", "--pack", "cm225:4k"]
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'type' = (hx vs lp)"
            in result.output
        )

        # apio build --type lp --size 8k
        result = click_cmd_runner.invoke(
            cmd_build, ["--type", "lp", "--size", "8k"]
        )
        assert result.exit_code != 0, result.output
        assert (
            "Error: contradictory argument values: 'type' = (hx vs lp)"
            in result.output
        )
