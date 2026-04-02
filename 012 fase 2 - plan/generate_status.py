from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import subprocess
import sys


@dataclass(frozen=True)
class Task:
    name: str
    phase: str
    start: date
    end: date
    evidence_key: str


TASKS = [
    Task("Proposal godkjent", "Initiering", date(2026, 2, 8), date(2026, 2, 8), "proposal"),
    Task("Planleggingsfase ferdig", "Planlegging", date(2026, 3, 9), date(2026, 3, 9), "plan"),
    Task("Datainnsamling", "Datagrunnlag", date(2026, 3, 10), date(2026, 3, 17), "raw_data"),
    Task("Datavask", "Datagrunnlag", date(2026, 3, 18), date(2026, 3, 23), "processed_data"),
    Task("Strukturering av datasett", "Datagrunnlag", date(2026, 3, 24), date(2026, 3, 26), "processed_data"),
    Task("Deskriptiv analyse", "Datagrunnlag", date(2026, 3, 27), date(2026, 3, 29), "analysis"),
    Task("Definere variabler", "Modellutvikling", date(2026, 3, 30), date(2026, 4, 1), "model"),
    Task("Formulere målfunksjon", "Modellutvikling", date(2026, 4, 2), date(2026, 4, 3), "model"),
    Task("Definere restriksjoner", "Modellutvikling", date(2026, 4, 4), date(2026, 4, 8), "model"),
    Task("Implementere modell", "Modellutvikling", date(2026, 4, 9), date(2026, 4, 20), "model"),
    Task("Teste modell", "Modellutvikling", date(2026, 4, 21), date(2026, 4, 28), "model"),
    Task("Basiskjøring", "Analyse", date(2026, 4, 29), date(2026, 5, 1), "analysis"),
    Task("Sensitivitetsanalyse", "Analyse", date(2026, 5, 2), date(2026, 5, 6), "analysis"),
    Task("Resultattolkning", "Analyse", date(2026, 5, 7), date(2026, 5, 11), "analysis"),
    Task("Skrive resultater", "Rapportering", date(2026, 5, 9), date(2026, 5, 14), "report"),
    Task("Diskusjon", "Rapportering", date(2026, 5, 12), date(2026, 5, 17), "report"),
    Task("Ferdigstille rapport", "Rapportering", date(2026, 5, 18), date(2026, 5, 23), "report"),
    Task("Revisjon", "Rapportering", date(2026, 5, 24), date(2026, 5, 29), "report"),
    Task("Språkvask / referanser", "Rapportering", date(2026, 5, 26), date(2026, 5, 30), "report"),
    Task("Prosjektbuffer", "Avslutning", date(2026, 5, 31), date(2026, 6, 2), "none"),
    Task("Innlevering", "Avslutning", date(2026, 6, 2), date(2026, 6, 2), "none"),
]

MILESTONES = [
    ("Proposal godkjent", date(2026, 2, 8)),
    ("Planleggingsfase ferdig", date(2026, 3, 9)),
    ("Datagrunnlag ferdig", date(2026, 3, 29)),
    ("Modelltesting ferdig", date(2026, 4, 28)),
    ("Innlevering", date(2026, 6, 2)),
]

CURRENT_FILE_NAMES = {"generate_status.py", "oppdater_status.ps1", "status.md"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def plan_dir() -> Path:
    return Path(__file__).resolve().parent


def parse_date_arg() -> date:
    if len(sys.argv) > 1:
        return date.fromisoformat(sys.argv[1])
    return datetime.now().date()


def list_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return [p for p in path.rglob("*") if p.is_file() and p.name != ".gitkeep"]


def find_files(root: Path, suffixes: tuple[str, ...], keywords: tuple[str, ...] = ()) -> list[Path]:
    matches: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == ".gitkeep":
            continue
        if path.name in CURRENT_FILE_NAMES and path.parent == plan_dir():
            continue
        if suffixes and path.suffix.lower() not in suffixes:
            continue
        rel = path.relative_to(root).as_posix().lower()
        if keywords and not any(keyword in rel for keyword in keywords):
            continue
        matches.append(path)
    return matches


def collect_evidence(root: Path) -> dict[str, object]:
    proposal_file = root / "011 fase 1 - proposal" / "proposal.md"
    plan_md = plan_dir() / "Prosjektstyringsplan, Odfjell Tankers.md"
    plan_mpp = plan_dir() / "MS_Project.mpp"

    data_files = list_files(root / "004 data")
    report_files = list_files(root / "005 report") + list_files(root / "014 fase 4 - report")
    processed_data = find_files(
        root,
        (".csv", ".xlsx", ".xls", ".parquet", ".md"),
        ("clean", "rens", "processed", "struktur", "datavask", "quality", "kvalitet"),
    )
    model_files = find_files(
        root,
        (".py", ".ipynb", ".jl", ".r"),
        ("model", "modell", "opt", "analysis", "analyse", "solver"),
    )
    analysis_files = find_files(
        root,
        (".py", ".ipynb", ".md", ".docx", ".xlsx"),
        ("analyse", "analysis", "resultat", "sensitivity", "sensitiv", "tolkning"),
    )

    return {
        "proposal": proposal_file.exists(),
        "plan": plan_md.exists() and plan_mpp.exists(),
        "raw_data": bool(data_files),
        "processed_data": bool(processed_data),
        "analysis": bool(analysis_files),
        "model": bool(model_files),
        "report": bool(report_files),
        "data_files": data_files,
        "report_files": report_files,
        "model_files": model_files,
        "analysis_files": analysis_files,
        "processed_data_files": processed_data,
    }


def task_state(task: Task, today: date, evidence: dict[str, object]) -> tuple[str, str]:
    key = task.evidence_key
    if key != "none" and evidence.get(key):
        return "Fullført", "Dokumentert i repo"
    if task.start <= today <= task.end:
        return "Pågår", f"Planlagt aktivitet nå ({task.start.isoformat()}–{task.end.isoformat()})"
    if today < task.start:
        return "Kommende", f"Starter {task.start.isoformat()}"
    if key == "none":
        return "Kommende", "Planlagt milepæl/buffer"
    return "Bør være ferdig", "Ingen tydelig dokumentasjon funnet i repo"


def current_phase(today: date) -> str:
    active = [task for task in TASKS if task.start <= today <= task.end]
    if active:
        return active[0].phase
    past = [task for task in TASKS if task.end < today]
    return past[-1].phase if past else TASKS[0].phase


def next_tasks(today: date) -> list[Task]:
    upcoming = [task for task in TASKS if task.end >= today and task.name not in {"Prosjektbuffer", "Innlevering"}]
    return upcoming[:4]


def milestone_rows(today: date) -> list[str]:
    rows = []
    for name, milestone_date in MILESTONES:
        status = "Passert" if today >= milestone_date else "Kommende"
        rows.append(f"| {name} | {milestone_date.isoformat()} | {status} |")
    return rows


def recent_git_activity(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "log", "--date=short", "--pretty=format:%ad %h %s", "-n", "5"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
    except Exception:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def latest_file_line(title: str, files: list[Path], root: Path) -> str:
    if not files:
        return f"- {title}: Ingen filer funnet"
    latest = max(files, key=lambda path: path.stat().st_mtime)
    rel = latest.relative_to(root).as_posix()
    stamp = datetime.fromtimestamp(latest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    return f"- {title}: `{rel}` sist endret {stamp}"


def build_summary(today: date, evidence: dict[str, object]) -> list[str]:
    lines: list[str] = []
    phase = current_phase(today)
    lines.append(f"- Prosjektet er i fasen **{phase}** per {today.isoformat()}.")

    active = [task for task in TASKS if task.start <= today <= task.end]
    if active:
        current = active[0]
        lines.append(
            f"- Aktiviteten som er planlagt akkurat nå er **{current.name}** ({current.start.isoformat()}–{current.end.isoformat()})."
        )

    if evidence["plan"]:
        lines.append("- Planunderlaget er dokumentert i både prosjektstyringsplanen og `MS_Project.mpp`.")
    if evidence["raw_data"]:
        lines.append("- Repoet inneholder rådata i `004 data`, så datainnsamling ser ut til å være startet eller gjennomført.")
    if not evidence["processed_data"]:
        lines.append("- Det finnes foreløpig ingen tydelig fil for renset/strukturert datasett, så datavask må dokumenteres bedre.")
    if not evidence["model"]:
        lines.append("- Det finnes foreløpig ingen tydelig modellfil i repoet, så modellutvikling er ikke dokumentert ennå.")
    if not evidence["report"]:
        lines.append("- Rapportmappen er fortsatt tom, så rapportskrivingen ser ikke ut til å ha startet.")
    return lines


def build_attention_points(today: date, evidence: dict[str, object]) -> list[str]:
    points: list[str] = []
    for task in next_tasks(today):
        state, _ = task_state(task, today, evidence)
        if state in {"Pågår", "Bør være ferdig"}:
            points.append(f"- {task.name}: {state.lower()} innen perioden {task.start.isoformat()}–{task.end.isoformat()}.")
    if not evidence["processed_data"]:
        points.append("- Dokumenter datavask og datastruktur i egne filer før modellimplementeringen fortsetter.")
    if not evidence["model"]:
        points.append("- Opprett første modellutkast før `Implementere modell` starter 2026-04-09.")
    return points[:5]


def build_task_rows(today: date, evidence: dict[str, object]) -> list[str]:
    rows = []
    relevant_tasks = [task for task in TASKS if task.phase in {"Datagrunnlag", "Modellutvikling", "Analyse", "Rapportering", "Avslutning"}]
    for task in relevant_tasks:
        state, note = task_state(task, today, evidence)
        rows.append(f"| {task.phase} | {task.name} | {task.start.isoformat()} | {task.end.isoformat()} | {state} | {note} |")
    return rows


def discrepancy_note() -> str:
    return (
        "Tekstplanen nevner endelig innlevering **2026-05-31**, mens `MS_Project.mpp` viser "
        "**2026-06-02** inkludert prosjektbuffer. Statusen under følger datoene i `MS_Project.mpp`."
    )


def generate_markdown(today: date, root: Path, evidence: dict[str, object]) -> str:
    git_activity = recent_git_activity(root)
    summary_lines = "\n".join(build_summary(today, evidence))
    attention_lines = "\n".join(build_attention_points(today, evidence))
    milestone_table = "\n".join(milestone_rows(today))
    task_table = "\n".join(build_task_rows(today, evidence))

    recent_files = "\n".join(
        [
            latest_file_line("Siste datafil", evidence["data_files"], root),
            latest_file_line("Siste analysefil", evidence["analysis_files"], root),
            latest_file_line("Siste modellfil", evidence["model_files"], root),
            latest_file_line("Siste rapportfil", evidence["report_files"], root),
        ]
    )

    git_lines = "\n".join(f"- `{line}`" for line in git_activity) if git_activity else "- Ingen git-historikk tilgjengelig"

    return f"""# Status - Minimering av drivstoffkostnader hos Odfjell Tankers

_Sist oppdatert automatisk: {today.isoformat()}_

Denne filen er generert fra:
- `012 fase 2 - plan/Prosjektstyringsplan, Odfjell Tankers.md`
- `012 fase 2 - plan/MS_Project.mpp`
- faktiske filer og siste aktivitet i repoet

## Overordnet status

{summary_lines}

## Hva vi må gjøre nå

{attention_lines}

## Fremdrift mot milepæler

| Milepæl | Dato | Status |
| --- | --- | --- |
{milestone_table}

## Aktivitetsstatus

| Fase | Aktivitet | Start | Slutt | Status {today.isoformat()} | Grunnlag |
| --- | --- | --- | --- | --- | --- |
{task_table}

## Spor i repoet

{recent_files}

### Siste git-aktivitet

{git_lines}

## Merknad om datoer

{discrepancy_note()}

## Oppdatering

Kjør `python "012 fase 2 - plan/generate_status.py"` for å regenerere denne filen med ny dato og oppdatert reposporing.
"""


def main() -> None:
    today = parse_date_arg()
    root = repo_root()
    evidence = collect_evidence(root)
    output = generate_markdown(today, root, evidence)
    target = plan_dir() / "status.md"
    target.write_text(output, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
