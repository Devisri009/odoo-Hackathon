"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Employee, employeesService } from "../../../../../services/employees";
import { authService } from "../../../../../services/auth";
import { StatusBadge } from "../../../../../components/shared/StatusBadge";
import { Card, CardContent, CardHeader, CardTitle } from "../../../../../components/ui/card";
import { Button } from "../../../../../components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "../../../../../components/ui/avatar";
import { ArrowLeft, Edit, Wallet } from "lucide-react";
import Link from "next/link";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../../../../components/ui/tabs";

export default function AdminEmployeeProfilePage() {
  const params = useParams();
  const router = useRouter();
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [currentUser, setCurrentUser] = useState<Employee | null>(null);

  useEffect(() => {
    setCurrentUser(authService.getCurrentUser());
    
    if (params.id) {
      employeesService.getById(params.id as string).then(emp => {
        if (emp) setEmployee(emp);
      });
    }
  }, [params.id]);

  if (!employee) {
    return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading employee data...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => router.back()} className="h-8 w-8">
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h2 className="text-2xl font-bold">Employee Information</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 space-y-6">
          <Card className="shadow-sm">
            <CardContent className="pt-6 flex flex-col items-center text-center">
              <Avatar className="h-24 w-24 border border-border mb-4">
                <AvatarImage src={employee.avatar} alt={employee.name} />
                <AvatarFallback className="text-2xl">{employee.name.charAt(0)}</AvatarFallback>
              </Avatar>
              <h3 className="text-xl font-bold">{employee.name}</h3>
              <p className="text-primary font-medium">{employee.position}</p>
              <p className="text-sm text-muted-foreground mt-1">{employee.department}</p>
              
              <div className="mt-4">
                <StatusBadge status={employee.status} />
              </div>

              {currentUser?.role === "ADMIN" && (
                <Link href={`/admin/employees/${employee.id}/salary`} className="w-full mt-6">
                  <Button className="w-full bg-primary hover:bg-primary/90 text-white gap-2">
                    <Wallet className="w-4 h-4" />
                    Salary Configuration
                  </Button>
                </Link>
              )}
            </CardContent>
          </Card>

          <Card className="shadow-sm">
            <CardHeader>
              <CardTitle className="text-lg">Contact Info</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Email</span>
                <span className="font-medium">{employee.email}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Phone</span>
                <span className="font-medium">{employee.phone}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Location</span>
                <span className="font-medium">{employee.location}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Manager</span>
                <span className="font-medium">{employee.manager}</span>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="md:col-span-2">
          <Tabs defaultValue="private" className="w-full">
            <TabsList className="grid w-full grid-cols-2 lg:w-1/2">
              <TabsTrigger value="private">Private Info</TabsTrigger>
              <TabsTrigger value="resume">Resume/Skills</TabsTrigger>
            </TabsList>
            
            <TabsContent value="private" className="mt-6 space-y-6">
              <Card className="shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg">Personal Details</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground mb-1">Date of Birth</p>
                    <p className="font-medium">{employee.dateOfBirth || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Nationality</p>
                    <p className="font-medium">{employee.nationality || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Gender</p>
                    <p className="font-medium">{employee.gender || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Marital Status</p>
                    <p className="font-medium">{employee.maritalStatus || "-"}</p>
                  </div>
                  <div className="md:col-span-2">
                    <p className="text-muted-foreground mb-1">Residing Address</p>
                    <p className="font-medium">{employee.residingAddress || "-"}</p>
                  </div>
                </CardContent>
              </Card>

              <Card className="shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg">Bank & Tax Details</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground mb-1">Bank Name</p>
                    <p className="font-medium">{employee.bankName || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Account Number</p>
                    <p className="font-medium">{employee.accountNumber || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">IFSC Code</p>
                    <p className="font-medium">{employee.ifscCode || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">PAN No</p>
                    <p className="font-medium">{employee.panNo || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">UAN No</p>
                    <p className="font-medium">{employee.uanNo || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Date of Joining</p>
                    <p className="font-medium">{employee.joiningDate || "-"}</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="resume" className="mt-6">
              <Card className="shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg">Skills & Experience</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-sm">No skills listed yet.</p>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
