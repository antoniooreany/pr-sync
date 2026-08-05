from unittest.mock import patch

from toolkit.cli import main


@patch("toolkit.cli.sys.argv", ["pr-sync"])
@patch("toolkit.cli.get_current_branch", return_value="feature/test")
@patch("toolkit.cli.get_diff", return_value="")
def test_cli_empty_diff(mock_diff, mock_branch):
    assert main() == 0


@patch("toolkit.cli.sys.argv", ["pr-sync"])
@patch("toolkit.cli.check_auth", return_value=True)
@patch("toolkit.cli.get_current_branch", return_value="feature/test")
@patch("toolkit.cli.get_diff", return_value="some diff")
@patch("toolkit.cli.find_open_pr", return_value=None)
@patch("toolkit.cli.create_pr", return_value={"url": "https://example.com/pr/1"})
def test_cli_create_pr(mock_create, mock_find, mock_diff, mock_branch, mock_auth):
    assert main() == 0
    mock_create.assert_called_once()


@patch("toolkit.cli.sys.argv", ["pr-sync"])
@patch("toolkit.cli.check_auth", return_value=True)
@patch("toolkit.cli.get_current_branch", return_value="feature/test")
@patch("toolkit.cli.get_diff", return_value="some diff")
@patch(
    "toolkit.cli.find_open_pr",
    return_value={"number": "123", "url": "https://example.com/pr/123", "title": "t", "body": "b"},
)
@patch("toolkit.cli.update_pr", return_value={"number": "123"})
def test_cli_update_pr(mock_update, mock_find, mock_diff, mock_branch, mock_auth):
    assert main() == 0
    mock_update.assert_called_once()


@patch("toolkit.cli.sys.argv", ["pr-sync"])
@patch("toolkit.cli.check_auth", return_value=False)
@patch("toolkit.cli.get_current_branch", return_value="feature/test")
@patch("toolkit.cli.get_diff", return_value="some diff")
def test_cli_no_auth(mock_diff, mock_branch, mock_auth):
    assert main() == 2
