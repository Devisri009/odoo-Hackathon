"use client";

import { useEffect, useState } from "react";
import { authService } from "../../../../services/auth";
import type { Employee } from "../../../../data/mockData";
import { Card, CardContent, CardHeader, CardTitle } from "../../../../components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../../../../components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../../../components/ui/tabs";
import { Button } from "../../../../components/ui/button";
import { Input } from "../../../../components/ui/input";

export default function EmployeeProfilePage() {
  const [user, setUser] = useState<Employee | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setUser(authService.getCurrentUser());
    setLoading(false);
  }, []);

  if (loading || !user) {
    return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading profile...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">My Profile</h2>
        <p className="text-muted-foreground mt-1">View and manage your personal information.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 space-y-6">
          <Card className="shadow-sm">
            <CardContent className="pt-6 flex flex-col items-center text-center">
              <Avatar className="h-24 w-24 border border-border mb-4">
                <AvatarImage src={user.avatar} alt={user.name} />
                <AvatarFallback className="text-2xl">{user.name.charAt(0)}</AvatarFallback>
              </Avatar>
              <h3 className="text-xl font-bold">{user.name}</h3>
              <p className="text-primary font-medium">{user.position}</p>
              <p className="text-sm text-muted-foreground mt-1">{user.department}</p>
            </CardContent>
          </Card>

          <Card className="shadow-sm">
            <CardHeader>
              <CardTitle className="text-lg">Contact Info</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Email</span>
                <span className="font-medium">{user.email}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Phone</span>
                <span className="font-medium">{user.phone}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Location</span>
                <span className="font-medium">{user.location}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Manager</span>
                <span className="font-medium">{user.manager}</span>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="md:col-span-2">
          <Tabs defaultValue="resume" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="resume">Resume</TabsTrigger>
              <TabsTrigger value="private">Private Info</TabsTrigger>
              <TabsTrigger value="security">Security</TabsTrigger>
            </TabsList>
            
            <TabsContent value="resume" className="mt-6 space-y-6">
              <Card className="shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg">About Me</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    I am a dedicated professional at Dayflow, constantly striving to improve processes and deliver value.
                  </p>
                </CardContent>
              </Card>
              <Card className="shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between">
                  <CardTitle className="text-lg">Skills</CardTitle>
                  <Button variant="outline" size="sm">Add Skill</Button>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2 flex-wrap">
                    <span className="px-3 py-1 bg-secondary/10 text-primary rounded-full text-xs font-medium border border-primary/20">Communication</span>
                    <span className="px-3 py-1 bg-secondary/10 text-primary rounded-full text-xs font-medium border border-primary/20">Leadership</span>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="private" className="mt-6 space-y-6">
              <Card className="shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg">Personal Details</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground mb-1">Date of Birth</p>
                    <p className="font-medium">{user.dateOfBirth || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Nationality</p>
                    <p className="font-medium">{user.nationality || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Gender</p>
                    <p className="font-medium">{user.gender || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Marital Status</p>
                    <p className="font-medium">{user.maritalStatus || "-"}</p>
                  </div>
                  <div className="md:col-span-2">
                    <p className="text-muted-foreground mb-1">Residing Address</p>
                    <p className="font-medium">{user.residingAddress || "-"}</p>
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
                    <p className="font-medium">{user.bankName || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">Account Number</p>
                    <p className="font-medium">{user.accountNumber || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">IFSC Code</p>
                    <p className="font-medium">{user.ifscCode || "-"}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground mb-1">PAN No</p>
                    <p className="font-medium">{user.panNo || "-"}</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="security" className="mt-6">
              <Card className="shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg">Change Password</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2 max-w-sm">
                    <label className="text-sm font-medium">Current Password</label>
                    <Input type="password" />
                  </div>
                  <div className="space-y-2 max-w-sm">
                    <label className="text-sm font-medium">New Password</label>
                    <Input type="password" />
                  </div>
                  <div className="space-y-2 max-w-sm">
                    <label className="text-sm font-medium">Confirm New Password</label>
                    <Input type="password" />
                  </div>
                  <Button className="mt-4 bg-primary hover:bg-primary/90 text-white">Update Password</Button>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
