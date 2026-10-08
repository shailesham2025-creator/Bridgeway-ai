const form = document.getElementById("skillForm");
const tagBox = document.getElementById("tagBox");
const input = document.getElementById("tagInput");
const hidden = document.getElementById("skillsHidden");

let tags = [];

function render() {
    tagBox.querySelectorAll(".tag").forEach(t => t.remove());

    tags.forEach((text, index) => {
        const tag = document.createElement("span");
        tag.className = "tag";
        tag.textContent = text;

        const remove = document.createElement("button");
        remove.type = "button";
        remove.innerHTML = "&times;";
        remove.onclick = () => {
            tags.splice(index, 1);
            render();
        };

        tag.appendChild(remove);
        tagBox.insertBefore(tag, input);
    });

    hidden.value = tags.join(",");
}

function addTag(value) {
    value.split(",").forEach(part => {
        const skill = part.trim().toLowerCase();
        if (skill && !tags.includes(skill)) {
            tags.push(skill);
        }
    });
    input.value = "";
    render();
}

input.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === ",") {
        e.preventDefault();
        addTag(input.value);
    } else if (e.key === "Backspace" && !input.value && tags.length) {
        tags.pop();
        render();
    }
});

input.addEventListener("blur", () => addTag(input.value));
tagBox.addEventListener("click", () => input.focus());
form.addEventListener("submit", () => addTag(input.value));