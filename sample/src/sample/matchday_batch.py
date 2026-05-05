"""Sample 3: 試合データのリストから複数スライドを一括生成。

1試合 = 1スライドのレイアウトを関数化し、データのリストをループで回して
1ファイルにまとめて出力する。実運用ではこのデータ部分を API 取得や CSV 読み込みに
差し替える想定。

実行:
    rye run python src/sample/matchday_batch.py
出力:
    matchday_batch.pptx, matchday_batch.pdf
"""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from pdf_export import convert_to_pdf


# プレミアリーグ第35節を想定したダミーデータ
MATCHDAY = 35
FIXTURES = [
    {
        "home": "Arsenal", "away": "Chelsea",
        "home_score": 2, "away_score": 1,
        "date": "2026-05-02 (Sat) 12:30",
        "stadium": "Emirates Stadium",
        "home_scorers": [("B. Saka", 18), ("K. Havertz", 67)],
        "away_scorers": [("C. Palmer", 55)],
    },
    {
        "home": "Liverpool", "away": "Manchester City",
        "home_score": 3, "away_score": 2,
        "date": "2026-05-03 (Sun) 17:30",
        "stadium": "Anfield",
        "home_scorers": [("M. Salah", 12), ("D. Núñez", 41), ("L. Díaz", 78)],
        "away_scorers": [("E. Haaland", 23), ("P. Foden", 65)],
    },
    {
        "home": "Manchester United", "away": "Tottenham",
        "home_score": 1, "away_score": 1,
        "date": "2026-05-03 (Sun) 14:00",
        "stadium": "Old Trafford",
        "home_scorers": [("R. Højlund", 33)],
        "away_scorers": [("S. Son", 88)],
    },
    {
        "home": "Newcastle", "away": "Aston Villa",
        "home_score": 0, "away_score": 2,
        "date": "2026-05-02 (Sat) 15:00",
        "stadium": "St James' Park",
        "home_scorers": [],
        "away_scorers": [("O. Watkins", 27), ("M. Rashford", 74)],
    },
    {
        "home": "Chelsea", "away": "Liverpool",  # 比較用に逆カードも
        "home_score": 0, "away_score": 0,
        "date": "2026-05-04 (Mon) 20:00",
        "stadium": "Stamford Bridge",
        "home_scorers": [],
        "away_scorers": [],
    },
]

TEAM_COLORS = {
    "Arsenal": "EF0107",
    "Chelsea": "034694",
    "Liverpool": "C8102E",
    "Manchester City": "6CABDD",
    "Manchester United": "DA291C",
    "Tottenham": "132257",
    "Newcastle": "241F20",
    "Aston Villa": "670E36",
}

PL_PURPLE = "37003C"


def add_text(slide, left, top, width, height, text, *,
             size=18, bold=False, color="000000", align=PP_ALIGN.CENTER):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)
    return box


def add_filled_rect(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(color)
    shape.line.fill.background()
    return shape


def add_team_panel(slide, left, top, width, height, team):
    color = TEAM_COLORS.get(team, "555555")
    panel = add_filled_rect(slide, left, top, width, height, color)
    tf = panel.text_frame
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.4)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = team
    run.font.size = Pt(26)
    run.font.bold = True
    run.font.color.rgb = RGBColor.from_string("FFFFFF")


def add_scorer_list(slide, left, top, width, height, scorers, *, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    if not scorers:
        p = tf.paragraphs[0]
        p.alignment = align
        run = p.add_run()
        run.text = "—"
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor.from_string("AAAAAA")
        return
    for i, (name, minute) in enumerate(scorers):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = f"⚽ {name}  {minute}'"
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor.from_string("222222")


def add_match_slide(prs, match, matchday):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_filled_rect(slide, Inches(0), Inches(0), Inches(13.33), Inches(0.9), PL_PURPLE)
    add_text(slide, Inches(0), Inches(0.2), Inches(13.33), Inches(0.6),
             f"Premier League · Matchday {matchday}",
             size=24, bold=True, color="FFFFFF")

    add_team_panel(slide, Inches(0.5), Inches(1.3), Inches(4.5), Inches(2.0), match["home"])
    add_team_panel(slide, Inches(8.33), Inches(1.3), Inches(4.5), Inches(2.0), match["away"])

    score = f"{match['home_score']}  -  {match['away_score']}"
    add_text(slide, Inches(5.0), Inches(1.4), Inches(3.33), Inches(1.4),
             score, size=72, bold=True, color="111111")
    add_text(slide, Inches(5.0), Inches(2.7), Inches(3.33), Inches(0.5),
             "FT", size=18, bold=True, color="888888")

    add_text(slide, Inches(0.5), Inches(3.5), Inches(12.33), Inches(0.4),
             match["date"], size=16, color="333333")
    add_text(slide, Inches(0.5), Inches(3.95), Inches(12.33), Inches(0.4),
             match["stadium"], size=14, color="666666")

    add_filled_rect(slide, Inches(0.5), Inches(4.6), Inches(12.33), Inches(0.5), "EEEEEE")
    add_text(slide, Inches(0.5), Inches(4.65), Inches(12.33), Inches(0.4),
             "Goals", size=16, bold=True, color="333333")

    add_scorer_list(slide, Inches(0.7), Inches(5.2), Inches(6.0), Inches(2.0),
                    match["home_scorers"], align=PP_ALIGN.LEFT)
    add_scorer_list(slide, Inches(7.0), Inches(5.2), Inches(6.0), Inches(2.0),
                    match["away_scorers"], align=PP_ALIGN.RIGHT)


def add_cover_slide(prs, matchday, fixtures):
    """先頭に「Matchday X / 試合数」のカバーを置く."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_filled_rect(slide, Inches(0), Inches(0), Inches(13.33), Inches(7.5), PL_PURPLE)
    add_text(slide, Inches(0), Inches(2.5), Inches(13.33), Inches(1.0),
             "Premier League", size=44, bold=True, color="FFFFFF")
    add_text(slide, Inches(0), Inches(3.6), Inches(13.33), Inches(1.0),
             f"Matchday {matchday}", size=60, bold=True, color="FFFFFF")
    add_text(slide, Inches(0), Inches(5.0), Inches(13.33), Inches(0.6),
             f"{len(fixtures)} fixtures", size=22, color="EEEEEE")


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    add_cover_slide(prs, MATCHDAY, FIXTURES)
    for match in FIXTURES:
        add_match_slide(prs, match, MATCHDAY)

    out = "matchday_batch.pptx"
    prs.save(out)
    print(f"saved: {out}  ({len(FIXTURES)} matches + 1 cover)")
    pdf = convert_to_pdf(out)
    print(f"saved: {pdf.name}")


if __name__ == "__main__":
    build()
