import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { apiLearningService } from "../../services/apiLearningService";

export function LevelSelector({
  label = "Cấp độ",
  toForLevel,
  value
}: {
  label?: string;
  toForLevel: (levelId: string) => string;
  value: string;
}) {
  const navigate = useNavigate();
  const levelsQuery = useQuery({
    queryKey: ["learning-levels"],
    queryFn: apiLearningService.getLevelSummaries
  });

  return (
    <label className="level-selector">
      <span>{label}</span>
      <select
        onChange={(event) => navigate(toForLevel(event.target.value))}
        value={value}
      >
        {levelsQuery.data ? null : <option value={value}>{value.toUpperCase()}</option>}
        {(levelsQuery.data ?? []).map((level) => (
          <option key={level.id} value={level.id}>
            {level.code}
          </option>
        ))}
      </select>
    </label>
  );
}
