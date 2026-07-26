(() => {
  const items = Array.isArray(window.MENU_ITEMS) ? window.MENU_ITEMS : [];
  const grid = document.querySelector("#menuGrid");
  const filters = document.querySelector("#categoryFilters");
  const heading = document.querySelector("#menuHeading");
  const count = document.querySelector("#menuCount");
  const empty = document.querySelector("#emptyState");
  const formatter = new Intl.NumberFormat("ko-KR");

  const categories = ["전체", ...new Set(items.map((item) => item.category))];
  let activeCategory = "전체";

  function cardTemplate(item) {
    const soldout = item.soldout ? '<span class="soldout">품절</span>' : "";
    return `
      <article class="menu-card">
        <div class="menu-card__image-wrap">
          <img class="menu-card__image" src="${item.image}" alt="${item.name}" loading="lazy" decoding="async">
          ${soldout}
        </div>
        <div class="menu-card__body">
          <span class="menu-card__category">${item.category}</span>
          <h3 class="menu-card__name">${item.name}</h3>
          <p class="menu-card__price">${formatter.format(item.price)}원</p>
        </div>
      </article>`;
  }

  function render() {
    const visible = activeCategory === "전체"
      ? items
      : items.filter((item) => item.category === activeCategory);

    heading.textContent = activeCategory === "전체" ? "전체 메뉴" : activeCategory;
    count.textContent = `${visible.length}개`;
    grid.innerHTML = visible.map(cardTemplate).join("");
    empty.hidden = visible.length > 0;

    filters.querySelectorAll("button").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.category === activeCategory));
    });
  }

  categories.forEach((category) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "filter";
    button.dataset.category = category;
    button.textContent = category;
    button.setAttribute("aria-pressed", String(category === activeCategory));
    button.addEventListener("click", () => {
      activeCategory = category;
      render();
      window.scrollTo({ top: document.querySelector(".category-nav").offsetTop, behavior: "smooth" });
    });
    filters.appendChild(button);
  });

  render();
})();
