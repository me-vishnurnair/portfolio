# Vishnu R. Nair - Portfolio, explained simply

## The idea

A responsive personal website presenting four real builds and an honest learning profile.

Start by running the application and completing one real action. Then follow the files below. You do not need to memorize the code; you need to explain how data moves and what can fail.

## Where to look

| File | Responsibility |
|---|---|
| `index.html` | Provides the page landmarks, content and dialog. |
| `style.css` | Defines the visual design and mobile breakpoints. |
| `app.js` | Defines project data and safe DOM rendering. |
| `assets/` | Contains actual screenshots from the locally running apps. |
| `.github/workflows/pages.yml` | Publishes only the public static assets after an explicit trigger. |

## Why these technologies

Semantic HTML and CSS suit a static presentation. Native JavaScript is enough for project details. GitHub Pages can serve the output without a server process. Keeping the dependency footprint small makes this a good first project to understand.

## Trace one action

1. The browser downloads index.html, style.css and app.js.
2. CSS creates the layout and adjusts it to the viewport.
3. JavaScript turns the project data into elements and text nodes.
4. A project button fills and opens a native modal dialog.
5. Close or Escape returns the visitor to the page.
6. Contact links use the verified existing account until public settings are changed.

## Ten likely interview questions

### 1. Why vanilla JavaScript instead of a framework?

The site is mostly static content with a small project dialog. Native browser features keep setup simple, avoid unnecessary dependencies and are easier to inspect while learning.

### 2. What does semantic HTML provide?

Elements such as header, nav, main, section and footer give the page meaningful structure for browsers and assistive technology.

### 3. How is the page responsive?

Grid layouts become a single column at smaller widths, font sizes and spacing adjust, and navigation simplifies without making the page wider than the viewport.

### 4. Why use a native dialog?

showModal supplies modal behavior and keyboard focus handling. A labelled close button and Escape make it usable without a mouse.

### 5. Why create text nodes?

Text nodes display strings as data instead of interpreting them as HTML. The helper avoids using innerHTML with project data.

### 6. Why are screenshots hosted locally?

They avoid dependence on a third-party image URL and make the repository self-contained. They also document the real interface state.

### 7. What does reduced-motion support do?

It turns off smooth scrolling when the visitor requests reduced motion. Respecting user preferences is part of accessible design.

### 8. How is the site deployed?

The GitHub Pages workflow copies the HTML, CSS, JavaScript, favicon and screenshots into an artifact and deploys that artifact. There is no application server.

### 9. Why are some links not active yet?

A link should represent a real destination. The project leaves demo URLs unset until deployment is verified and clearly displays that status.

### 10. How will you keep the profile honest?

Separate current foundations from technologies still being learned, describe observable project behavior, and add experience or performance numbers only when there is evidence.

## A practical exercise

Add one project reflection paragraph describing a bug you personally fixed. Test keyboard access and check the 390 px layout again.

## Honest scope

Read the limits in the README. The implementation and its tests are real; external deployment, production operation, independent mastery and employer experience are not implied.
