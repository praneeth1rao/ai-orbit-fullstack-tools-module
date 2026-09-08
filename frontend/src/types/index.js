export function toFormData(value) {
  return value;
}

export const Pricing = {
  FREE: "free",
  FREEMIUM: "freemium",
  PAID: "paid",
};

export const Status = {
  DRAFT: "draft",
  PUBLISHED: "published",
  ARCHIVED: "archived",
};

export const SortOptions = [
  { label: "Newest", value: "newest" },
  { label: "Oldest", value: "oldest" },
  { label: "Name A-Z", value: "name_asc" },
  { label: "Name Z-A", value: "name_desc" },
];

export const PricingOptions = [
  { label: "All", value: "" },
  { label: "Free", value: "free" },
  { label: "Freemium", value: "freemium" },
  { label: "Paid", value: "paid" },
];

export const StatusOptions = [
  { label: "Draft", value: "draft" },
  { label: "Published", value: "published" },
  { label: "Archived", value: "archived" },
];

export const PlatformOptions = [
  { label: "Web", value: "web" },
  { label: "Windows", value: "windows" },
  { label: "macOS", value: "macos" },
  { label: "iOS", value: "ios" },
  { label: "Android", value: "android" },
  { label: "API", value: "api" },
];
