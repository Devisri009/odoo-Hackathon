"use client";

import { useEffect, useState } from "react";
import { authService } from "../../../../services/auth";
import { attendanceService } from "../../../../services/attendance";
import { employeesService } from "../../../../services/employees";
import type { AttendanceRecord, Employee } from "../../../../data/mockData";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../../../components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "../../../../components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../../../../components/ui/avatar";
import { Input } from "../../../../components/ui/input";
import { Search } from "lucide-react";

type EnrichedRecord = AttendanceRecord & { employee?: Employee };

export default function AdminAttendancePage() {
  const [records, setRecords] = useState<EnrichedRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const fetchInitial = async () => {
      const user = authService.getCurrentUser();
      if (user?.role !== "ADMIN" && user?.role !== "HR_OFFICER") return;

      const allRecords = await attendanceService.getAll();
      const allEmployees = await employeesService.getAll();
      
      const enriched = allRecords.map(r => ({
        ...r,
        employee: allEmployees.find(e => e.id === r.employeeId)
      }));
      
      // Sort descending by date
      setRecords(enriched.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()));
      setLoading(false);
    };
    fetchInitial();
  }, []);

  const filteredRecords = records.filter(r => 
    r.employee?.name.toLowerCase().includes(search.toLowerCase()) || 
    r.date.includes(search)
  );

  if (loading) {
    return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading all attendance records...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Company Attendance</h2>
          <p className="text-muted-foreground mt-1">View attendance records across all employees.</p>
        </div>
      </div>

      <div className="flex items-center gap-2 max-w-sm">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search by name or date..."
            className="pl-8 bg-white border-border"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle>All Records</CardTitle>
        </CardHeader>
        <CardContent>
          {filteredRecords.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <p>No attendance records found.</p>
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader className="bg-gray-50/50">
                  <TableRow>
                    <TableHead>Employee</TableHead>
                    <TableHead>Date</TableHead>
                    <TableHead>Check In</TableHead>
                    <TableHead>Check Out</TableHead>
                    <TableHead className="text-right">Work Hours</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredRecords.map((record) => (
                    <TableRow key={record.id}>
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={record.employee?.avatar} />
                            <AvatarFallback>{record.employee?.name?.charAt(0)}</AvatarFallback>
                          </Avatar>
                          <span className="font-medium">{record.employee?.name || "Unknown"}</span>
                        </div>
                      </TableCell>
                      <TableCell>{record.date}</TableCell>
                      <TableCell>{record.checkIn}</TableCell>
                      <TableCell>{record.checkOut || "-"}</TableCell>
                      <TableCell className="text-right">{record.workHours ? `${record.workHours}h` : "-"}</TableCell>
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
