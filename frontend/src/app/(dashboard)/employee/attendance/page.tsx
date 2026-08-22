"use client";

import { useEffect, useState } from "react";
import { authService } from "../../../../services/auth";
import { attendanceService } from "../../../../services/attendance";
import type { Employee, AttendanceRecord } from "../../../../data/mockData";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../../../components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "../../../../components/ui/card";
import { Calendar, Clock, ArrowLeft, ArrowRight } from "lucide-react";
import { Button } from "../../../../components/ui/button";

export default function EmployeeAttendancePage() {
  const [user, setUser] = useState<Employee | null>(null);
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInitial = async () => {
      const currUser = authService.getCurrentUser();
      if (currUser) {
        setUser(currUser);
        const userRecords = await attendanceService.getByEmployee(currUser.id);
        // Sort descending by date
        setRecords(userRecords.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()));
      }
      setLoading(false);
    };
    fetchInitial();
  }, []);

  if (loading || !user) {
    return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading attendance records...</div>;
  }

  const totalWorkHours = records.reduce((acc, curr) => acc + curr.workHours, 0);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Attendance</h2>
        <p className="text-muted-foreground mt-1">View your check-in and check-out history.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Working Days</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{records.length}</div>
            <p className="text-xs text-muted-foreground mt-1 text-green-600 font-medium">Days present</p>
          </CardContent>
        </Card>
        <Card className="shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Hours</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{totalWorkHours.toFixed(1)}h</div>
            <p className="text-xs text-muted-foreground mt-1">Logged work hours</p>
          </CardContent>
        </Card>
      </div>

      <Card className="shadow-sm">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Attendance History</CardTitle>
          <div className="flex gap-2">
            <Button variant="outline" size="icon" className="h-8 w-8"><ArrowLeft className="h-4 w-4" /></Button>
            <Button variant="outline" size="icon" className="h-8 w-8"><ArrowRight className="h-4 w-4" /></Button>
          </div>
        </CardHeader>
        <CardContent>
          {records.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <p>No attendance records found.</p>
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader className="bg-gray-50/50">
                  <TableRow>
                    <TableHead>Date</TableHead>
                    <TableHead>Check In</TableHead>
                    <TableHead>Check Out</TableHead>
                    <TableHead className="text-right">Work Hours</TableHead>
                    <TableHead className="text-right">Extra Hours</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {records.map((record) => (
                    <TableRow key={record.id}>
                      <TableCell className="font-medium">{record.date}</TableCell>
                      <TableCell>{record.checkIn}</TableCell>
                      <TableCell>{record.checkOut || "-"}</TableCell>
                      <TableCell className="text-right">{record.workHours ? `${record.workHours}h` : "-"}</TableCell>
                      <TableCell className="text-right">{record.extraHours ? `${record.extraHours}h` : "-"}</TableCell>
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
