"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { authService } from "../../../../../services/auth";
import { timeoffService } from "../../../../../services/timeoff";
import { Card, CardContent, CardHeader, CardTitle } from "../../../../../components/ui/card";
import { Button } from "../../../../../components/ui/button";
import { Input } from "../../../../../components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../../../../components/ui/select";
import { ArrowLeft } from "lucide-react";
import { toast } from "sonner";
import Link from "next/link";

export default function NewTimeOffRequestPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [type, setType] = useState("Paid Time Off");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [days, setDays] = useState(1);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const user = authService.getCurrentUser();
    if (!user) return;

    if (!startDate || !endDate || days <= 0) {
      toast.error("Invalid input", { description: "Please ensure all fields are filled out correctly." });
      return;
    }

    setLoading(true);
    await timeoffService.create({
      employeeId: user.id,
      type: type as any,
      startDate,
      endDate,
      days
    });
    
    toast.success("Request Submitted", { description: "Your time-off request is now pending approval." });
    setLoading(false);
    router.push("/employee/time-off");
  };

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <div className="flex items-center gap-4">
        <Link href="/employee/time-off">
          <Button variant="outline" size="icon" className="h-8 w-8">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <h2 className="text-2xl font-bold">New Time Off Request</h2>
      </div>

      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle>Request Details</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium">Time Off Type</label>
              <Select value={type} onValueChange={setType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Paid Time Off">Paid Time Off</SelectItem>
                  <SelectItem value="Sick Leave">Sick Leave</SelectItem>
                  <SelectItem value="Unpaid Leave">Unpaid Leave</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Start Date</label>
                <Input 
                  type="date" 
                  value={startDate} 
                  onChange={e => setStartDate(e.target.value)} 
                  required 
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">End Date</label>
                <Input 
                  type="date" 
                  value={endDate} 
                  onChange={e => setEndDate(e.target.value)} 
                  required 
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Number of Days</label>
              <Input 
                type="number" 
                min="0.5" step="0.5"
                value={days} 
                onChange={e => setDays(parseFloat(e.target.value) || 0)} 
                required 
              />
            </div>
            
            {type === "Sick Leave" && (
              <div className="space-y-2">
                <label className="text-sm font-medium flex justify-between">
                  Attachment 
                  <span className="text-muted-foreground text-xs font-normal">Optional certificate</span>
                </label>
                <Input type="file" className="cursor-pointer" />
              </div>
            )}

            <div className="flex gap-4 pt-4 border-t">
              <Button type="submit" disabled={loading} className="bg-primary hover:bg-primary/90 text-white flex-1">
                {loading ? "Submitting..." : "Submit Request"}
              </Button>
              <Link href="/employee/time-off" className="flex-1">
                <Button type="button" variant="outline" className="w-full">
                  Discard
                </Button>
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
