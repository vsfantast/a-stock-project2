# PDF Report Skill

Base directory: /Users/kendu/Documents/项目/.claude/skills/pdf-report

This skill produces beautiful, production-grade PDF reports from HTML/CSS. It combines
precision typography, magazine-quality layouts, and reliable rendering via headless Chromium.

## When to Use

- User asks for a PDF report, document, proposal, or analysis output
- User wants a stock analysis report, financial summary, or investment memo
- User mentions "PDF", "报告", "导出", "report", "download"

## Design Philosophy

Every report must have a clear **typographic identity** and **visual hierarchy**. Do not
produce generic-looking documents. Choose from these aesthetic directions based on context:

| Direction | Best for | Key traits |
|-----------|----------|------------|
| **Financial/Professional** | Stock reports, investment memos | Dark header, red accent, data-dense tables |
| **Editorial/Minimal** | Research papers, market commentary | Generous whitespace, serif body, restrained color |
| **Modern/Tech** | Product analysis, tech sector | Gradient accents, card layouts, sans-serif |

Before generating, commit to a direction. Then execute it consistently throughout:
typography, color palette, spacing rhythm, table styling.

## Workflow

### Step 1: Gather content
Collect all data, analysis, and text before writing HTML. Structure it logically:
executive summary → body sections → conclusion.

### Step 2: Choose template
Apply one of the CSS templates from `templates/` as the base. Customize colors and
typography to match the content's tone.

### Step 3: Build HTML
Write complete, self-contained HTML with:
- All CSS inline or in a `<style>` tag (no external dependencies)
- Responsive layout that respects `@page` for print
- Real data in tables (never placeholder text in final output)
- Proper semantic structure: `h1-h3`, `table`, `section`, `article`

### Step 4: Generate PDF
Run the conversion script:
```
python3 /Users/kendu/Documents/项目/.claude/skills/pdf-report/scripts/generate_pdf.py <input.html> <output.pdf>
```

The script auto-installs Playwright Chromium on first run if needed (~150MB download).

### Step 5: Verify
Open the PDF and check: page breaks, table alignment, Chinese rendering, overall visual
balance. Fix any issues and regenerate.

## Typography Rules

### Chinese text
- Primary: `PingFang SC` (macOS system, excellent hinting)
- Fallback: `STHeiti`, `Hiragino Sans GB`, `Microsoft YaHei`
- Body size: 10-11pt for reports, 9-10pt for data-heavy tables
- Line height: 1.7-1.8 for body text, 1.4-1.5 for tables

### Numeric data (prices, percentages, financials)
- Use **tabular figures** via `font-variant-numeric: tabular-nums` so columns align
- Encode with `<span class="tn">123.45</span>` for tabular number styling
- Right-align all numeric columns in tables

### Mixed Chinese-English
- Always put a space between Chinese and English/Latin text: `三花智控 (002050.SZ)`
- Use full-width punctuation for Chinese text (，。) but half-width for numbers (123.45)
- For units: `2268亿`, `53.91元` — no space between number and Chinese unit

## Color System

### Financial report palette (default)
```
--bg-primary: #ffffff
--bg-secondary: #f8f9fa
--bg-dark: #1a1a2e
--text-primary: #1a1a1a
--text-secondary: #555555
--text-muted: #888888
--accent: #c0392b        # Deep red — buy, positive, important
--accent-green: #27ae60   # Sell, negative
--accent-blue: #2980b9    # Neutral, informational
--border: #e0e0e0
--border-light: #f0f0f0
```

### Editorial/minimal palette
```
--bg-primary: #fafaf8
--text-primary: #2c2c2c
--accent: #8b0000
--border: #d5d5d0
```

### Tech/modern palette
```
--bg-dark: #0d1117
--bg-card: #161b22
--text-primary: #e6edf3
--accent: #58a6ff
--accent-green: #3fb950
--border: #30363d
```

## Table Design

Tables are the backbone of financial reports. Follow these rules:

1. **Header row**: Dark background (`#2c3e50` or similar), white text, bold, uppercase
2. **Zebra striping**: Subtle (`#f8f9fa` on even rows), never high-contrast
3. **Alignment**: Text left, numbers right, indicators center
4. **Column width**: Size proportionally to content, don't let short labels hog space
5. **Numeric formatting**: Right-align, use `font-variant-numeric: tabular-nums`
6. **Color coding**: 
   - Positive/up: `#c0392b` (red in Chinese markets)
   - Negative/down: `#27ae60` (green in Chinese markets)
   - Do NOT use Western green=up/red=down convention for A-share reports

## Page Layout

```css
@page {
  size: A4;
  margin: 20mm 18mm 25mm 18mm;
  @top-center {
    content: "Report Title — Date";
    font-size: 8pt;
    color: #999;
  }
  @bottom-center {
    content: "Page " counter(page);
    font-size: 8pt;
    color: #999;
  }
}
```

- Cover page: no header/footer
- First page of content: no header (optional)
- All other pages: header + page number footer

## Special Components

### Metric cards
Use for key numbers (price, PE, market cap). Dark background, large value,
small muted label. Group in a flex row of 4-6.

### Callout boxes
For warnings, signals, or key takeaways. Left border accent, subtle background.
Three variants: `callout-bull` (red, bullish), `callout-bear` (green, bearish),
`callout-info` (blue, neutral).

### Verdict box
Dark background card for the final investment conclusion. White/colored text,
structured as key-value pairs (rating, target price, entry zone, stop loss).

## Dependencies

- Python 3.8+ with `pip install playwright`
- First run: `python3 -m playwright install chromium` (one-time, ~150MB)
- Chinese fonts: uses system fonts (PingFang SC on macOS, no extra install needed)

## Templates Available

| Template | File | Use case |
|----------|------|----------|
| Stock Deep Analysis | `templates/stock-deep.css` | Full 10-module stock report with all sections |
| Market Briefing | `templates/market-brief.css` | Short daily/weekly market summary |
| Investment Memo | `templates/investment-memo.css` | Clean, text-heavy investment thesis |

## Quality Checklist

Before delivering a PDF, verify:
- [ ] All Chinese text renders correctly (no tofu/missing glyphs)
- [ ] Tables don't break mid-row across pages
- [ ] Numbers in tables are right-aligned and use tabular-nums
- [ ] Page numbers appear on every page (except cover)
- [ ] Color coding is consistent (red=positive, green=negative for A-shares)
- [ ] No horizontal scroll/overflow — all content fits within page margins
- [ ] Headers/footers don't overlap with body content
- [ ] The report has a clear visual hierarchy (title → section → detail)
