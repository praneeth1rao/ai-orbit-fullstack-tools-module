import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { toolsApi, categoriesApi, APIError } from "../services/api";
import { PricingOptions, PlatformOptions, StatusOptions } from "../types";
import {
  FormInputField,
  FormTextareaField,
  FormSelectField,
  FormCheckboxesField,
  FormTagsField,
  FormUrlField,
} from "../components/FormFields";

export default function NewToolPage() {
  const navigate = useNavigate();

  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [createdToolId, setCreatedToolId] = useState(null);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [longDescription, setLongDescription] = useState("");
  const [categorySlug, setCategorySlug] = useState("");
  const [pricing, setPricing] = useState("free");
  const [platforms, setPlatforms] = useState([]);
  const [tags, setTags] = useState([]);
  const [websiteUrl, setWebsiteUrl] = useState("");
  const [status, setStatus] = useState("published");

  const [errors, setErrors] = useState({});

  useEffect(() => {
    categoriesApi.list().then(setCategories).catch(() => setCategories([]));
  }, []);

  const validate = () => {
    const newErrors = {};

    if (!title.trim()) {
      newErrors.title = "Title is required.";
    }

    if (!description.trim()) {
      newErrors.description = "Description is required.";
    }

    if (!categorySlug) {
      newErrors.category = "Please select a category.";
    }

    if (!pricing) {
      newErrors.pricing = "Please select a pricing option.";
    }

    if (!status) {
      newErrors.status = "Please select a status.";
    }

    if (websiteUrl) {
      try {
        new URL(websiteUrl);
      } catch {
        newErrors.websiteUrl = "Please enter a valid URL (e.g., example.com).";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setSaving(true);
    setError(null);

    try {
      const data = await toolsApi.create({
        title: title.trim(),
        description: description.trim(),
        long_description: longDescription.trim() || null,
        category_slug: categorySlug || null,
        pricing,
        platforms: platforms.length > 0 ? platforms : undefined,
        tags: tags.length > 0 ? tags : undefined,
        website_url: websiteUrl || null,
        status,
        logo_url: null,
      });

      setSuccess(true);
      setCreatedToolId(data.id);
    } catch (err) {
      setError(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <section className="page tool-form-page">
        <div className="tool-form-header">
          <h1 className="tool-form-title">New tool</h1>
          <p className="tool-form-subtitle">
            Add a new AI tool to the directory.
          </p>
        </div>
        <div className="tool-form-loading">
          <div className="loading-state">
            <div className="loading-bar" />
            <p className="loading-text">Loading form…</p>
          </div>
        </div>
      </section>
    );
  }

  if (success && createdToolId) {
    return (
      <section className="page tool-form-page">
        <div className="tool-form-header">
          <h1 className="tool-form-title">Tool created</h1>
        </div>
        <div className="tool-form-success">
          <div className="success-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
              <circle cx="20" cy="20" r="18" stroke="currentColor" strokeWidth="1.5" />
              <path
                d="M13 20l5 5 10-12"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <h2 className="success-title">Tool created successfully</h2>
          <p className="success-message">
            Your tool has been added to the directory.
          </p>
          <div className="success-actions">
            <Link
              className="btn btn-primary"
              to={`/tools/${createdToolId}`}
            >
              View tool
            </Link>
            <button
              className="btn btn-secondary"
              type="button"
              onClick={() => navigate("/tools", { replace: true })}
            >
              Back to Tools
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="page tool-form-page">
      <div className="tool-form-header">
        <div className="tool-form-nav">
          <Link className="btn btn-ghost" to="/tools">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path
                d="M10 3l-6 5 6 5"
                stroke="currentColor"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Back to Tools
          </Link>
        </div>
        <h1 className="tool-form-title">New tool</h1>
        <p className="tool-form-subtitle">
          Add a new AI tool to the directory.
        </p>
      </div>

      <div className="tool-form-card">
        {error && (
          <div className="tool-form-error-banner">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="1.5" />
              <path
                d="M12 8v5M12 16h.01"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
            <div>
              <p className="tool-form-error-text">
                {error instanceof APIError
                  ? error.message
                  : error?.message
                  ? error.message
                  : "Something went wrong. Please try again."}
              </p>
              <button
                className="btn btn-secondary"
                type="button"
                onClick={() => setError(null)}
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        <form className="tool-form" onSubmit={handleSubmit} noValidate>
          <div className="tool-form-section">
            <h2 className="tool-form-section-title">Basic information</h2>

            <div className="tool-form-grid">
              <FormInputField
                label="Title"
                value={title}
                onChange={(e) => {
                  setTitle(e.target.value);
                  if (errors.title) setErrors({ ...errors, title: null });
                }}
                error={errors.title}
                required
                placeholder="Enter the tool name"
              />

              <FormSelectField
                label="Category"
                value={categorySlug}
                onChange={(e) => {
                  setCategorySlug(e.target.value);
                  if (errors.category) setErrors({ ...errors, category: null });
                }}
                error={errors.category}
                required
                options={[
                  { label: "Select a category…", value: "" },
                  ...categories.map((c) => ({ label: c.name, value: c.slug })),
                ]}
              />

              <FormSelectField
                label="Pricing"
                value={pricing}
                onChange={(e) => {
                  setPricing(e.target.value);
                  if (errors.pricing) setErrors({ ...errors, pricing: null });
                }}
                error={errors.pricing}
                required
                options={PricingOptions.filter((p) => p.value !== "")}
              />

              <FormSelectField
                label="Status"
                value={status}
                onChange={(e) => {
                  setStatus(e.target.value);
                  if (errors.status) setErrors({ ...errors, status: null });
                }}
                error={errors.status}
                required
                options={StatusOptions}
              />
            </div>
          </div>

          <div className="tool-form-section">
            <h2 className="tool-form-section-title">Description</h2>

            <div className="tool-form-grid">
              <FormTextareaField
                label="Description"
                value={description}
                onChange={(e) => {
                  setDescription(e.target.value);
                  if (errors.description) setErrors({ ...errors, description: null });
                }}
                error={errors.description}
                required
                placeholder="A brief overview of the tool (shown in listings)"
                rows={3}
              />

              <div className="tool-form-full-width">
                <FormTextareaField
                  label="Long description"
                  value={longDescription}
                  onChange={(e) => setLongDescription(e.target.value)}
                  placeholder="A detailed description of the tool"
                  rows={6}
                />
              </div>
            </div>
          </div>

          <div className="tool-form-section">
            <h2 className="tool-form-section-title">Platforms & tags</h2>

            <div className="tool-form-grid">
              <FormCheckboxesField
                label="Platforms"
                value={platforms}
                onChange={setPlatforms}
                options={PlatformOptions}
              />

              <FormTagsField
                label="Tags"
                value={tags}
                onChange={setTags}
                placeholder="Type and press Enter to add…"
              />
            </div>
          </div>

          <div className="tool-form-section">
            <h2 className="tool-form-section-title">Links</h2>

            <div className="tool-form-grid">
              <FormUrlField
                label="Website URL"
                value={websiteUrl}
                onChange={(e) => {
                  setWebsiteUrl(e.target.value);
                  if (errors.websiteUrl) setErrors({ ...errors, websiteUrl: null });
                }}
                error={errors.websiteUrl}
                placeholder="example.com"
              />
            </div>
          </div>

          <div className="tool-form-footer">
            <div className="tool-form-actions">
              <Link className="btn btn-ghost" to="/tools">
                Cancel
              </Link>
              <button
                className="btn btn-primary"
                type="submit"
                disabled={saving}
              >
                {saving ? (
                  <>
                    <span className="btn-spinner" />
                    Saving…
                  </>
                ) : (
                  "Create tool"
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </section>
  );
}
