// =============================================================
// COMPONENT RENDERERS
//
// Each renderer takes the `props` object the model returned and
// gives back a string of HTML for the side panel.
//
// The model can get things wrong: a prop might be missing, or a
// list might come back as a string. Each renderer below uses a
// default (`|| ''`, asList(...)) so a bad answer still shows something.
// =============================================================

// Text from the model must go through esc() before it goes into HTML.
// Otherwise a passage containing "<script>" could run code on your page.
function esc(value) {
    const div = document.createElement('div');
    div.textContent = value == null ? '' : String(value);
    return div.innerHTML;
}

// Returns `value` if it is a list, otherwise an empty list.
function asList(value) {
    return Array.isArray(value) ? value : [];
}

const RENDERERS = {

    definition_card(props) {
        return `
            <div class="c-definition">
                <div class="c-term">${esc(props.term)}</div>
                <p>${esc(props.definition)}</p>
                ${props.example ? `<p class="c-example">e.g. ${esc(props.example)}</p>` : ''}
            </div>`;
    },

    step_list(props) {
        const steps = asList(props.steps).map(step => `<li>${esc(step)}</li>`).join('');
        return `
            <div class="c-steps">
                <h3>${esc(props.title)}</h3>
                <ol>${steps}</ol>
            </div>`;
    },

    comparison_table(props) {
        const header = asList(props.columns).map(col => `<th>${esc(col)}</th>`).join('');
        const rows = asList(props.rows).map(row =>
            `<tr>${asList(row).map(cell => `<td>${esc(cell)}</td>`).join('')}</tr>`
        ).join('');
        return `
            <div class="c-compare">
                <h3>${esc(props.title)}</h3>
                <table>
                    <thead><tr>${header}</tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>`;
    },

    // Fallback used by app.py when the model's answer couldn't be used.
    text_card(props) {
        return `<div class="c-text">${esc(props.text)}</div>`;
    },

    // =========================================================
    // YOUR TASK (Part 2, step 1 of 2): Add a renderer for a new
    // component. Copy one of the renderers above and change it.
    //
    //   - The name (e.g. timeline, quiz_question, key_terms) must
    //     match the entry you add to COMPONENTS in app.py.
    //   - Wrap every value from the model in esc().
    //   - Wrap every list from the model in asList().
    //   - Optional: add CSS for it in static/components.css.
    // =========================================================

};

// Called by reader.html with the spec returned from /generate.
function renderComponent(spec) {
    const renderer = RENDERERS[spec.component];
    if (!renderer) {
        return RENDERERS.text_card({ text: `No renderer for "${spec.component}" yet.` });
    }
    return renderer(spec.props || {});
}
