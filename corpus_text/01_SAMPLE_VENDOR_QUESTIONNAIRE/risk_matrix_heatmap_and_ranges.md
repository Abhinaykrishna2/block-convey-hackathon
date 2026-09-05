# Vendor questionnaire: risk matrix graphic

- **Source path (repository-relative):** `Hackathon/1. Sample_Vendor questionnaire/Regodit_Comprehensive_Vendor_Security_Questionnaire_Clean.xlsx`
- **Source locator:** hidden worksheet `Risk Matrix`; `xl/worksheets/sheet9.xml` -> `xl/drawings/drawing9.xml` -> `xl/media/image1.png`. One-cell anchor starts at A6 (zero-based column 0, row 5, with offsets).
- **Image:** 936 x 414 pixels; preserved copy `Hackathon/extracted_media/questionnaire_image1.png`.
- **Evidence type:** literal image text and visual structure, followed by separately labelled interpretation. The graphic is a screenshot, not a workbook formula.

## Literal visual text and values

Vertical axis: `Probability`. Horizontal axis: `Impact`.

| Probability / Impact | Low | Medium | High | Critical |
|---|---|---|---|---|
| Critical | 4 | 8 | 12 | 16 |
| High | 3 | 6 | 9 | 12 |
| Medium | 2 | 4 | 6 | 8 |
| Low | 1 | 2 | 3 | 4 |

Visible fill colors (descriptive colors, not a printed legend): scores 1, 2, and 3 are light blue; 4 and 6 are orange; 8, 9, and 12 are red; 16 is dark red. Green plus icons appear above the probability labels and to the right of the bottom impact labels; red minus icons appear above the Critical impact column and beside the Critical probability row.

Below the matrix:

> Risk level ranges
>
> Define the risk score ranges for each risk level.

The horizontal bar has light-blue, orange, red, and dark-red segments from left to right. Its three displayed slider values are `4.00`, `8.00`, and `12.10`. Visible axis tick labels are `2`, `4`, `6`, `8`, `10`, `12`, `14`, and `16`. The endpoints have no printed numeric labels.

## Interpretation and limits

The matrix numbers are consistent with multiplying ordinal probability and impact weights Low=1, Medium=2, High=3, Critical=4. That formula and those numeric weights are inferred from the displayed products; neither is printed as a formula or axis weight in the image.

The image does not specify inclusive/exclusive threshold rules, rounding precision, formal tier names for the colored slider segments, required remediation, onboarding approval, or escalation authorities. In particular, `4.01`, `8.01`, and `12.11` are not printed. The heatmap colors place 4 in orange and 8 in red, so do not silently assign those boundary values to the preceding color based on a presumed inclusive slider range. Workbook calculation logic must be assessed separately.
