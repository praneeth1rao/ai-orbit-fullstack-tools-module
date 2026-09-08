import { useState, useRef, useEffect } from "react";

export default function SearchBar({ value, onChange, placeholder, autoFocus }) {
  const [local, setLocal] = useState(value || "");
  const inputRef = useRef(null);

  useEffect(() => {
    setLocal(value || "");
  }, [value]);

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocus]);

  const handleChange = (e) => {
    const next = e.target.value;
    setLocal(next);
    onChange(next);
  };

  const clear = () => {
    setLocal("");
    onChange("");
    inputRef.current?.focus();
  };

  return (
    <div className="search-bar">
      <svg className="search-icon" width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <circle cx="9" cy="9" r="5.5" stroke="currentColor" strokeWidth="1.5" />
        <path d="M13.5 13.5L17 17" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
      <input
        ref={inputRef}
        className="search-input"
        type="search"
        value={local}
        onChange={handleChange}
        placeholder={placeholder || "Search tools..."}
        aria-label="Search tools"
      />
      {local && (
        <button className="search-clear" type="button" onClick={clear} aria-label="Clear search">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M4 4l8 8M12 4l-8 8"
              stroke="currentColor"
              strokeWidth="1.75"
              strokeLinecap="round"
            />
          </svg>
        </button>
      )}
    </div>
  );
}
