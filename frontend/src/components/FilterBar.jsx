import { useMemo } from "react";
import { PricingOptions, PlatformOptions, SortOptions } from "../types";

export default function FilterBar({
  categories,
  selectedCategory,
  onCategoryChange,
  selectedPricing,
  onPricingChange,
  selectedPlatforms,
  onPlatformsChange,
  selectedSort,
  onSortChange,
  onClearFilters,
  activeFilterCount,
}) {
  const platformList = useMemo(
    () => PlatformOptions.map((p) => ({ ...p, checked: selectedPlatforms.includes(p.value) })),
    [selectedPlatforms]
  );

  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label className="filter-label" htmlFor="tool-category">
          Category
        </label>
        <select
          id="tool-category"
          className="filter-select"
          value={selectedCategory}
          onChange={(e) => onCategoryChange(e.target.value)}
        >
          <option value="">All categories</option>
          {categories?.map((c) => (
            <option key={c.id} value={c.slug}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label" htmlFor="tool-pricing">
          Pricing
        </label>
        <select
          id="tool-pricing"
          className="filter-select"
          value={selectedPricing}
          onChange={(e) => onPricingChange(e.target.value)}
        >
          {PricingOptions.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <span className="filter-label">Platform</span>
        <div className="platform-list" role="group" aria-label="Platform filters">
          {platformList.map((p) => (
            <label key={p.value} className="platform-chip">
              <input
                type="checkbox"
                className="platform-checkbox"
                checked={p.checked}
                onChange={(e) => {
                  if (e.target.checked) {
                    onPlatformsChange([...selectedPlatforms, p.value]);
                  } else {
                    onPlatformsChange(selectedPlatforms.filter((v) => v !== p.value));
                  }
                }}
              />
              <span className="platform-name">{p.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="filter-group">
        <label className="filter-label" htmlFor="tool-sort">
          Sort
        </label>
        <select
          id="tool-sort"
          className="filter-select"
          value={selectedSort}
          onChange={(e) => onSortChange(e.target.value)}
        >
          {SortOptions.map((s) => (
            <option key={s.value} value={s.value}>
              {s.label}
            </option>
          ))}
        </select>
      </div>

      {activeFilterCount > 0 && (
        <button className="filter-clear" type="button" onClick={onClearFilters}>
          Clear filters
        </button>
      )}
    </div>
  );
}
