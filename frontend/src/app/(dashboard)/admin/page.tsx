"use client";

import { useEffect, useState } from "react";
import { authService } from "../../../services/auth";
import type { Employee } from "../../../data/mockData";
import { Card, CardContent, CardHeader, CardTitle } from "../../../components/ui/card";
import { Users, Calendar, Clock } from "lucide-react";
import Link from "next/link";

export default function AdminDashboard() {
  const [user, setUser] = useState<Employee | null>(null);

  useEffect(() => {
    setUser(authService.getCurrentUser());
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Welcome, {user?.name}</h2>
        <p className="text-muted-foreground mt-1">Here is the overview for today.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Link href="/admin/employees">
          <Card className="hover:border-primary/50 transition-colors shadow-sm cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Employees</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">5</div>
              <p className="text-xs text-muted-foreground mt-1 text-green-600 font-medium">3 Present</p>
            </CardContent>
          </Card>
        </Link>
        <Link href="/admin/attendance">
          <Card className="hover:border-primary/50 transition-colors shadow-sm cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Attendance (Today)</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">60%</div>
              <p className="text-xs text-muted-foreground mt-1">Attendance rate</p>
            </CardContent>
          </Card>
        </Link>
        <Link href="/admin/time-off">
          <Card className="hover:border-primary/50 transition-colors shadow-sm cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Pending Requests</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">1</div>
              <p className="text-xs text-muted-foreground mt-1 text-yellow-600 font-medium">Time-off request to review</p>
            </CardContent>
          </Card>
        </Link>
      </div>
    </div>
  );
}
