import { PageHeader } from "../components/common/PageHeader";
import { EmptyState } from "../components/common/StateViews";

export function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="page-stack">
      <PageHeader title={title} subtitle="Khu vực này đã có layout sẵn và sẽ kết nối dữ liệu ở bước tiếp theo." />
      <EmptyState text="Nội dung đang được cập nhật." title="Sắp ra mắt" />
    </div>
  );
}
