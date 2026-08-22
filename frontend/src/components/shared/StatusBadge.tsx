import { Badge } from "../ui/badge";

export function StatusBadge({ status, text }: { status: "GREEN" | "BLUE" | "YELLOW" | "Pending" | "Approved" | "Rejected", text?: string }) {
  if (status === "GREEN" || status === "Approved") {
    return (
      <Badge variant="outline" className="bg-secondary/20 text-green-700 border-green-200 gap-1">
        <span className="w-2 h-2 rounded-full bg-green-500"></span>
        {text || "Present"}
      </Badge>
    );
  }
  
  if (status === "BLUE") {
    return (
      <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200 gap-1">
        <span className="w-2 h-2 rounded-full bg-blue-500"></span>
        {text || "On Leave"}
      </Badge>
    );
  }

  if (status === "YELLOW" || status === "Pending") {
    return (
      <Badge variant="outline" className="bg-yellow-50 text-yellow-700 border-yellow-200 gap-1">
        <span className="w-2 h-2 rounded-full bg-yellow-500"></span>
        {text || (status === "Pending" ? "Pending" : "Absent")}
      </Badge>
    );
  }
  
  if (status === "Rejected") {
    return (
      <Badge variant="outline" className="bg-red-50 text-destructive border-red-200 gap-1">
        <span className="w-2 h-2 rounded-full bg-destructive"></span>
        {text || "Rejected"}
      </Badge>
    );
  }

  return <Badge variant="outline">{text || status}</Badge>;
}
