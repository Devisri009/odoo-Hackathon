"use client";

import { useEffect, useState } from "react";
import { authService } from "../../../services/auth";
import { attendanceService } from "../../../services/attendance";
import type { Employee, AttendanceRecord } from "../../../data/mockData";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../../../components/ui/card";
import { Button } from "../../../components/ui/button";
import { LogIn, LogOut, Clock, Calendar } from "lucide-react";
import { toast } from "sonner";
import Link from "next/link";

export default function EmployeeDashboard() {
  const [user, setUser] = useState<Employee | null>(null);
  const [loadingAction, setLoadingAction] = useState(false);
  const [todayRecord, setTodayRecord] = useState<AttendanceRecord | null>(null);

  useEffect(() => {
    const fetchInitial = async () => {
      const currUser = authService.getCurrentUser();
      if (currUser) {
        setUser(currUser);
        const records = await attendanceService.getByEmployee(currUser.id);
        const today = new Date().toISOString().split('T')[0];
        const recordForToday = records.find(r => r.date === today);
        if (recordForToday) setTodayRecord(recordForToday);
      }
    };
    fetchInitial();
  }, []);

  const handleCheckIn = async () => {
    if (!user) return;
    setLoadingAction(true);
    const newRecord = await attendanceService.checkIn(user.id);
    setTodayRecord(newRecord);
    toast.success("Checked In", { description: `You have successfully checked in at ${newRecord.checkIn}.` });
    setLoadingAction(false);
  };

  const handleCheckOut = async () => {
    if (!todayRecord) return;
    setLoadingAction(true);
    const updatedRecord = await attendanceService.checkOut(todayRecord.id);
    if (updatedRecord) {
      setTodayRecord(updatedRecord);
      toast.success("Checked Out", { description: `You have successfully checked out at ${updatedRecord.checkOut}.` });
    }
    setLoadingAction(false);
  };

  if (!user) return null;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground mt-1">Welcome back, {user.name}.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="shadow-sm border-primary/20">
          <CardHeader className="bg-primary/5 pb-4">
            <CardTitle>Time Tracking</CardTitle>
            <CardDescription>Mark your attendance for today</CardDescription>
          </CardHeader>
          <CardContent className="pt-6 flex flex-col items-center text-center space-y-4">
            <div className="text-4xl font-light text-foreground mb-4">
              {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
            
            {todayRecord ? (
              todayRecord.checkOut ? (
                <div className="space-y-3 w-full">
                  <div className="p-4 bg-green-50 text-green-800 rounded-md border border-green-200">
                    <p className="font-semibold">Work completed for today</p>
                    <p className="text-sm mt-1">Logged {todayRecord.workHours} hours</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm pt-2">
                    <div className="bg-white p-3 border rounded">
                      <p className="text-muted-foreground mb-1">Check In</p>
                      <p className="font-medium">{todayRecord.checkIn}</p>
                    </div>
                    <div className="bg-white p-3 border rounded">
                      <p className="text-muted-foreground mb-1">Check Out</p>
                      <p className="font-medium">{todayRecord.checkOut}</p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-4 w-full">
                  <div className="p-3 bg-blue-50 text-blue-800 rounded-md border border-blue-200 flex justify-between items-center px-4">
                    <span className="text-sm font-medium">Checked in at</span>
                    <span className="font-bold">{todayRecord.checkIn}</span>
                  </div>
                  <Button 
                    onClick={handleCheckOut} 
                    disabled={loadingAction}
                    className="w-full bg-secondary hover:bg-secondary/90 text-white h-12 text-lg"
                  >
                    <LogOut className="mr-2 h-5 w-5" />
                    {loadingAction ? "Processing..." : "Check Out"}
                  </Button>
                </div>
              )
            ) : (
              <Button 
                onClick={handleCheckIn} 
                disabled={loadingAction}
                className="w-full bg-primary hover:bg-primary/90 text-white h-12 text-lg"
              >
                <LogIn className="mr-2 h-5 w-5" />
                {loadingAction ? "Processing..." : "Check In"}
              </Button>
            )}
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Link href="/employee/attendance" className="block">
            <Card className="hover:border-primary/50 transition-colors shadow-sm cursor-pointer h-full">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-lg font-medium">My Attendance</CardTitle>
                <Clock className="h-5 w-5 text-primary" />
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">View your recent attendance history and working hours.</p>
              </CardContent>
            </Card>
          </Link>

          <Link href="/employee/time-off" className="block">
            <Card className="hover:border-primary/50 transition-colors shadow-sm cursor-pointer h-full">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-lg font-medium">Time Off</CardTitle>
                <Calendar className="h-5 w-5 text-primary" />
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">Request leave and check your paid time off balances.</p>
              </CardContent>
            </Card>
          </Link>
        </div>
      </div>
    </div>
  );
}
