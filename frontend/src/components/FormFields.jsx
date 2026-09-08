export default function FormField({
  label,
  error,
  children,
  required,
  className = "",
}) {
  return (
    <div className={`form-field ${className}`}>
      <label className="form-label">
        {label}
        {required && <span className="form-required">*</span>}
      </label>
      {children}
      {error && <p className="form-error">{error}</p>}
    </div>
  );
}

export function FormTextareaField({
  label,
  value,
  onChange,
  error,
  required,
  placeholder,
  rows = 4,
}) {
  return (
    <FormField label={label} error={error} required={required}>
      <textarea
        className="form-textarea"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        aria-invalid={!!error}
      />
    </FormField>
  );
}

export function FormInputField({
  label,
  value,
  onChange,
  error,
  required,
  placeholder,
  type = "text",
}) {
  return (
    <FormField label={label} error={error} required={required}>
      <input
        className="form-input"
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        aria-invalid={!!error}
      />
    </FormField>
  );
}

export function FormSelectField({
  label,
  value,
  onChange,
  error,
  required,
  options,
}) {
  return (
    <FormField label={label} error={error} required={required}>
      <select
        className="form-select"
        value={value}
        onChange={onChange}
        aria-invalid={!!error}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </FormField>
  );
}

export function FormCheckboxesField({
  label,
  value,
  onChange,
  error,
  options,
}) {
  return (
    <FormField label={label} error={error}>
      <div className="form-checkboxes" role="group" aria-label={label}>
        {options.map((opt) => (
          <label key={opt.value} className="form-checkbox-label">
            <input
              type="checkbox"
              className="form-checkbox"
              checked={value.includes(opt.value)}
              onChange={(e) => {
                if (e.target.checked) {
                  onChange([...value, opt.value]);
                } else {
                  onChange(value.filter((v) => v !== opt.value));
                }
              }}
            />
            <span className="form-checkbox-text">{opt.label}</span>
          </label>
        ))}
      </div>
    </FormField>
  );
}

export function FormTagsField({
  label,
  value,
  onChange,
  error,
  placeholder = "Add a tag…",
}) {
  const tags = Array.isArray(value) ? value : [];

  const addTag = (tag) => {
    const trimmed = tag.trim();
    if (!trimmed) return;
    if (tags.some((t) => t.toLowerCase() === trimmed.toLowerCase())) return;
    onChange([...tags, trimmed]);
  };

  const removeTag = (tagToRemove) => {
    onChange(tags.filter((t) => t !== tagToRemove));
  };

  return (
    <FormField label={label} error={error}>
      <div className="form-tags">
        <div className="form-tags-list">
          {tags.map((tag) => (
            <span key={tag} className="form-tag">
              {tag}
              <button
                type="button"
                className="form-tag-remove"
                onClick={() => removeTag(tag)}
                aria-label={`Remove ${tag}`}
              >
                <svg width="12" height="12" viewBox="0 0 16 16" fill="none">
                  <path
                    d="M4 4l8 8M12 4l-8 8"
                    stroke="currentColor"
                    strokeWidth="1.75"
                    strokeLinecap="round"
                  />
                </svg>
              </button>
            </span>
          ))}
          <input
            className="form-tags-input"
            value=""
            onChange={(e) => addTag(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === ",") {
                e.preventDefault();
                addTag(e.target.value);
                e.target.value = "";
              }
            }}
            placeholder={tags.length === 0 ? placeholder : ""}
            aria-label={`Add tag`}
          />
        </div>
      </div>
    </FormField>
  );
}

export function FormUrlField({
  label,
  value,
  onChange,
  error,
  required,
  placeholder = "https://example.com",
}) {
  return (
    <FormField label={label} error={error} required={required}>
      <div className="form-url">
        <span className="form-url-prefix">https://</span>
        <input
          className="form-url-input"
          type="text"
          value={value ? value.replace(/^https?:\/\//, "") : ""}
          onChange={(e) => {
            const raw = e.target.value;
            if (raw.startsWith("http://") || raw.startsWith("https://")) {
              onChange(raw);
            } else {
              onChange(`https://${raw}`);
            }
          }}
          placeholder={placeholder}
          aria-invalid={!!error}
        />
      </div>
    </FormField>
  );
}
