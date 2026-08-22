"use client";

import { useEffect, useState } from "react";
import { authService } from "../../../../services/auth";
import { timeoffService } from "../../../../services/timeoff";
import { employeesService } from "../../../../services/employees";
import type { TimeOffRequest, Employee } from "../../../../data/mockData";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../../../components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "../../../../components/ui/card";
import { StatusBadge } from "../../../../components/shared/StatusBadge";
import { Avatar, AvatarFallback, AvatarImage } from "../../../../components/ui/avatar";
import { Button } from "../../../../components/ui/button";
import { Check, X } from "lucide-react";
import { toast } from "sonner";

type EnrichedRequest = TimeOffRequest & { employee?: Employee };

export default function AdminTimeOffPage() {
  const [requests, setRequests] = useState<EnrichedRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const user = authService.getCurrentUser();
    if (user?.role !== "ADMIN" && user?.role !== "HR_OFFICER") return;

    const allRequests = await timeoffService.getAll();
    const allEmployees = await employeesService.getAll();
    
    const enriched = allRequests.map(r => ({
      ...r,
      employee: allEmployees.find(e => e.id === r.employeeId)
    }));
    
    setRequests(enriched);
    setLoading(false);
  };

  const handleStatusUpdate = async (id: string, status: "Approved" | "Rejected") => {
    const updated = await timeoffService.updateStatus(id, status);
    if (updated) {
      toast.success(`Request ${status}`, { description: `The time-off request was successfully ${status.toLowerCase()}.` });
      setRequests(prev => prev.map(r => r.id === id ? { ...r, status } : r));
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading time-off requests...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Time Off Requests</h2>
        <p className="text-muted-foreground mt-1">Review and manage employee leave applications.</p>
      </div>

      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle>All Requests</CardTitle>
        </CardHeader>
        <CardContent>
          {requests.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <p>No time-off requests found.</p>
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader className="bg-gray-50/50">
                  <TableRow>
                    <TableHead>Employee</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Dates</TableHead>
                    <TableHead className="text-center">Days</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {requests.map((req) => (
                    <TableRow key={req.id}>
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={req.employee?.avatar} />
                            <AvatarFallback>{req.employee?.name?.charAt(0)}</AvatarFallback>
                          </Avatar>
                          <span className="font-medium">{req.employee?.name || "Unknown"}</span>
                        </div>
                      </TableCell>
                      <TableCell>{req.type}</TableCell>
                      <TableCell>
                        <div className="text-sm">
                          <div>{req.startDate}</div>
                          <div className="text-muted-foreground text-xs">to {req.endDate}</div>
                        </div>
                      </TableCell>
                      <TableCell className="text-center">{req.days}</TableCell>
                      <TableCell>
                        <StatusBadge status={req.status} />
                      </TableCell>
                      <TableCell className="text-right">
                        {req.status === "Pending" ? (
                          <div className="flex justify-end gap-2">
                            <Button 
                              size="sm" 
                              variant="outline" 
                              className="text-green-600 border-green-200 hover:bg-green-50"
                              onClick={() => handleStatusUpdate(req.id, "Approved")}
                            >
                              <Check className="h-4 w-4 mr-1" /> Approve
                            </Button>
                            <Button 
                              size="sm" 
                              variant="outline" 
                              className="text-destructive border-red-200 hover:bg-red-50"
                              onClick={() => handleStatusUpdate(req.id, "Rejected")}
                            >
                              <X className="h-4 w-4 mr-1" /> Reject
                            </Button>
                          </div>
                        ) : (
                          <span className="text-sm text-muted-foreground">Resolved</span>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
