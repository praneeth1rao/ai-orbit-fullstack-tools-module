export default function LoadingState({ text = "Loading..." }) {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <div className="loading-bar" />
      <p className="loading-text">{text}</p>
    </div>
  );
}
