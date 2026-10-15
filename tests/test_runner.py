import json

from vm.fingerprint import file_sha256
from vm.runner import main, read_info


def test_read_info(tmp_path):
    p = tmp_path / "student_info.txt"
    p.write_text(
        "# comment\nname: Ada Obi\nmatric_number: <your matriculation number>\n"
        "Supervisor: Dr X\nai_use: I asked an AI tool\n   to explain stability.\n",
        encoding="utf-8",
    )
    info = read_info(p)
    assert info["name"] == "Ada Obi"
    assert info["matric_number"] == ""  # placeholder left unchanged
    assert info["supervisor"] == "Dr X"
    assert info["ai_use"] == "I asked an AI tool to explain stability."
    assert info["department"] == ""


def test_fingerprint_ignores_line_endings(tmp_path):
    a, b = tmp_path / "a.py", tmp_path / "b.py"
    a.write_bytes(b"x = 1\ny = 2\n")
    b.write_bytes(b"x = 1\r\ny = 2\r\n")
    assert file_sha256(a) == file_sha256(b)


def test_main_on_the_shipped_stubs(root, tmp_path):
    out = tmp_path / "report"
    code = main(["--steps", str(root / "student" / "steps.py"), "--out", str(out)])
    assert code == 0
    data = json.loads((out / "verification-report.json").read_text(encoding="utf-8"))
    assert [r["status"] for r in data["results"]] == ["not implemented"] * 3
    html = (out / "verification-report.html").read_text(encoding="utf-8")
    assert "Verification report" in html and "does not show who wrote the code" in html


def test_student_text_is_escaped_and_failures_set_exit_code(tmp_path):
    student = tmp_path / "student"
    student.mkdir()
    (student / "steps.py").write_text(
        "import numpy as np\n"
        "def euler_step(f, t, y, h):\n    return y + 2 * h * np.asarray(f(t, y))\n",
        encoding="utf-8",
    )
    (student / "student_info.txt").write_text("name: <b>x</b><script>alert(1)</script>\n", encoding="utf-8")
    out = tmp_path / "report"
    code = main(["--steps", str(student / "steps.py"), "--out", str(out)])
    assert code == 1  # the wrong Euler step fails gates
    html = (out / "verification-report.html").read_text(encoding="utf-8")
    assert "<script>alert(1)</script>" not in html and "&lt;script&gt;" in html
    json.loads((out / "verification-report.json").read_text(encoding="utf-8"))  # valid JSON, no NaN


def test_syntax_error_gives_exit_code_2(tmp_path, capsys):
    bad = tmp_path / "steps.py"
    bad.write_text("def euler_step(f, t, y, h)\n    return y\n", encoding="utf-8")
    assert main(["--steps", str(bad), "--out", str(tmp_path / "r")]) == 2
    assert "line 1" in capsys.readouterr().out


def test_student_prints_are_captured_and_repeated_errors_said_once(tmp_path, capsys):
    student = tmp_path / "student"
    student.mkdir()
    (student / "steps.py").write_text(
        "def euler_step(f, t, y, h):\n    print('debug', t)\n    return y + h * undefined_name\n", encoding="utf-8"
    )
    main(["--steps", str(student / "steps.py"), "--out", str(tmp_path / "r")])
    out = capsys.readouterr().out
    assert "Your code printed" in out and out.count("debug") <= 5
    assert "G1, G2, G3, G4 FAILED: Your code raised NameError" in out
