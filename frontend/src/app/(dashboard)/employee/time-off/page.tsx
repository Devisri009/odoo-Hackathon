"use client";

import { useEffect, useState } from "react";
import { authService } from "../../../../services/auth";
import { timeoffService } from "../../../../services/timeoff";
import type { Employee, TimeOffRequest } from "../../../../data/mockData";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../../../components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "../../../../components/ui/card";
import { StatusBadge } from "../../../../components/shared/StatusBadge";
import { Calendar, Plus } from "lucide-react";
import { Button } from "../../../../components/ui/button";
import Link from "next/link";

export default function EmployeeTimeOffPage() {
  const [user, setUser] = useState<Employee | null>(null);
  const [requests, setRequests] = useState<TimeOffRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInitial = async () => {
      const currUser = authService.getCurrentUser();
      if (currUser) {
        setUser(currUser);
        const userRequests = await timeoffService.getByEmployee(currUser.id);
        setRequests(userRequests);
      }
      setLoading(false);
    };
    fetchInitial();
  }, []);

  if (loading || !user) {
    return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading time-off data...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Time Off</h2>
          <p className="text-muted-foreground mt-1">Manage your leaves and time-off requests.</p>
        </div>
        <Link href="/employee/time-off/new">
          <Button className="bg-primary hover:bg-primary/90 text-white gap-2 shadow-sm">
            <Plus className="w-4 h-4" />
            New Request
          </Button>
        </Link>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Paid Time Off Balance</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">12 Days</div>
            <p className="text-xs text-muted-foreground mt-1">Available to use</p>
          </CardContent>
        </Card>
        <Card className="shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Sick Leave Balance</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">6 Days</div>
            <p className="text-xs text-muted-foreground mt-1">Available to use</p>
          </CardContent>
        </Card>
      </div>

      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle>My Requests</CardTitle>
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
                    <TableHead>Type</TableHead>
                    <TableHead>Start Date</TableHead>
                    <TableHead>End Date</TableHead>
                    <TableHead className="text-right">Days</TableHead>
                    <TableHead className="text-right">Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {requests.map((req) => (
                    <TableRow key={req.id}>
                      <TableCell className="font-medium">{req.type}</TableCell>
                      <TableCell>{req.startDate}</TableCell>
                      <TableCell>{req.endDate}</TableCell>
                      <TableCell className="text-right">{req.days}</TableCell>
                      <TableCell className="text-right">
                        <StatusBadge status={req.status} />
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
