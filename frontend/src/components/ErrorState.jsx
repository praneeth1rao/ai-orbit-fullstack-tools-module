export default function ErrorState({ message, onRetry, errorText }) {
  return (
    <div className="error-state">
      <div className="error-icon" aria-hidden="true">
        <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
          <circle cx="20" cy="20" r="18" stroke="currentColor" strokeWidth="1.5" />
          <path
            d="M14 14l12 12M26 14l-12 12"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
      </div>
      <h3 className="error-title">Something went wrong</h3>
      <p className="error-message">
        {message || "We couldn’t load the tools right now."}
      </p>
      {errorText && <p className="error-detail">{errorText}</p>}
      {onRetry && (
        <button className="btn btn-primary" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}
