"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth";
import { employeesService } from "@/services/employees";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { ArrowLeft, Copy, Check, Upload, X, ShieldAlert, Award } from "lucide-react";
import Link from "next/link";

export default function NewEmployeePage() {
  const [currentUser, setCurrentUser] = useState<any>(null);
  const router = useRouter();

  // Form Fields
  const [companyName, setCompanyName] = useState("Dayflow");
  const [companyLogo, setCompanyLogo] = useState<string | null>(null);
  const [employeeName, setEmployeeName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [role, setRole] = useState<"EMPLOYEE" | "HR_OFFICER" | "ADMIN">("EMPLOYEE");
  const [department, setDepartment] = useState("");
  const [position, setPosition] = useState("");
  const [location, setLocation] = useState("");
  const [joiningDate, setJoiningDate] = useState("");

  const [loading, setLoading] = useState(false);
  const [createdCredentials, setCreatedCredentials] = useState<{ loginId: string; tempPassword: string } | null>(null);
  const [copiedLoginId, setCopiedLoginId] = useState(false);
  const [copiedPassword, setCopiedPassword] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const user = authService.getCurrentUser();
    if (!user) {
      router.push("/login");
    } else if (user.role === "EMPLOYEE") {
      toast.error("Access Denied", {
        description: "You do not have permission to access the employee creation page.",
      });
      router.push("/employee");
    } else {
      setCurrentUser(user);
    }
  }, [router]);

  const handleLogoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setCompanyLogo(reader.result as string);
        toast.success("Logo uploaded successfully");
      };
      reader.readAsDataURL(file);
    }
  };

  const removeLogo = () => {
    setCompanyLogo(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await employeesService.createEmployee({
        name: employeeName,
        email,
        phone,
        companyName,
        role,
        department,
        position,
        location,
        joiningDate: joiningDate || undefined,
      });

      setCreatedCredentials({
        loginId: result.loginId,
        tempPassword: result.tempPassword,
      });

      toast.success("Employee account created successfully!");
    } catch (err) {
      toast.error("Failed to create employee");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, type: "login" | "pass") => {
    navigator.clipboard.writeText(text);
    if (type === "login") {
      setCopiedLoginId(true);
      setTimeout(() => setCopiedLoginId(false), 2000);
    } else {
      setCopiedPassword(true);
      setTimeout(() => setCopiedPassword(false), 2000);
    }
    toast.success("Copied to clipboard!");
  };

  if (!currentUser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-muted-foreground text-sm">Verifying administration access...</p>
      </div>
    );
  }

  if (createdCredentials) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="flex items-center gap-2">
          <Button variant="ghost" onClick={() => setCreatedCredentials(null)} className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            Create Another
          </Button>
        </div>

        <Card className="border-emerald-200 bg-emerald-50/30">
          <CardHeader className="text-center pb-2">
            <div className="flex justify-center mb-2 text-emerald-600">
              <Award size={48} className="animate-bounce" />
            </div>
            <CardTitle className="text-2xl font-bold text-emerald-800">Account Created Successfully</CardTitle>
            <CardDescription className="text-emerald-700">
              Credentials generated for {employeeName} (Role: {role})
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6 max-w-md mx-auto pt-4">
            <div className="bg-white p-4 rounded-lg border border-emerald-100 shadow-sm space-y-4">
              <div className="space-y-1">
                <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">Login ID</span>
                <div className="flex items-center justify-between bg-gray-50 p-2.5 rounded border border-gray-200">
                  <code className="font-mono text-base font-bold text-gray-800">{createdCredentials.loginId}</code>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-8 w-8 p-0 hover:bg-emerald-100/50 hover:text-emerald-700"
                    onClick={() => copyToClipboard(createdCredentials.loginId, "login")}
                  >
                    {copiedLoginId ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4 text-gray-500" />}
                  </Button>
                </div>
              </div>

              <div className="space-y-1">
                <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">Temporary Password</span>
                <div className="flex items-center justify-between bg-gray-50 p-2.5 rounded border border-gray-200">
                  <code className="font-mono text-base font-bold text-gray-800">{createdCredentials.tempPassword}</code>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-8 w-8 p-0 hover:bg-emerald-100/50 hover:text-emerald-700"
                    onClick={() => copyToClipboard(createdCredentials.tempPassword, "pass")}
                  >
                    {copiedPassword ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4 text-gray-500" />}
                  </Button>
                </div>
              </div>
            </div>

            <div className="text-center space-y-4 pt-2">
              <p className="text-sm text-emerald-800">
                Please copy and share these credentials securely with the employee. They will be forced to change their password upon their first login.
              </p>
              <Link href="/admin/employees" passHref>
                <Button className="w-full bg-emerald-600 hover:bg-emerald-700 text-white">
                  Back to Employee List
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-2">
        <Link href="/admin/employees" passHref>
          <Button variant="ghost" className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back to Employees
          </Button>
        </Link>
      </div>

      <div>
        <h2 className="text-3xl font-bold tracking-tight">Create Employee Account</h2>
        <p className="text-muted-foreground mt-1">Provision a new employee user account and auto-generate credentials.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Company Section */}
        <Card className="border-border">
          <CardHeader>
            <CardTitle className="text-lg">Company Details</CardTitle>
            <CardDescription>Setup company affiliation and logo layout.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Company Name</label>
                <Input
                  value={companyName}
                  onChange={(e: any) => setCompanyName(e.target.value)}
                  placeholder="e.g. Dayflow"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Company Logo</label>
                <div className="flex items-center gap-4">
                  {companyLogo ? (
                    <div className="relative w-16 h-16 border rounded bg-white overflow-hidden flex items-center justify-center">
                      <img src={companyLogo} alt="Preview" className="max-w-full max-h-full object-contain" />
                      <button
                        type="button"
                        onClick={removeLogo}
                        className="absolute top-0.5 right-0.5 bg-red-500 hover:bg-red-600 text-white rounded-full p-0.5 shadow-sm"
                      >
                        <X className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ) : (
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => fileInputRef.current?.click()}
                      className="h-16 w-16 flex flex-col items-center justify-center border-dashed border-gray-300 gap-1"
                    >
                      <Upload className="w-4 h-4 text-muted-foreground" />
                      <span className="text-[10px] text-muted-foreground">Upload</span>
                    </Button>
                  )}
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleLogoUpload}
                    accept="image/*"
                    className="hidden"
                  />
                  <div className="text-xs text-muted-foreground">
                    <p>Click box to upload PNG/JPG.</p>
                    <p>Prepared for backend storage sync.</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Employee Section */}
        <Card className="border-border">
          <CardHeader>
            <CardTitle className="text-lg">Employee Details</CardTitle>
            <CardDescription>Fill out core personal and occupational info.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Employee Full Name</label>
                <Input
                  value={employeeName}
                  onChange={(e: any) => setEmployeeName(e.target.value)}
                  placeholder="e.g. John Doe"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Role Privilege</label>
                <Select
                  value={role}
                  onValueChange={(val: any) => setRole(val)}
                >
                  <SelectTrigger className="bg-white border-border">
                    <SelectValue placeholder="Select privilege level" />
                  </SelectTrigger>
                  <SelectContent className="bg-white border-border">
                    <SelectItem value="EMPLOYEE">Employee (Standard)</SelectItem>
                    <SelectItem value="HR_OFFICER">HR Officer</SelectItem>
                    <SelectItem value="ADMIN">Administrator</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Work Email</label>
                <Input
                  type="email"
                  value={email}
                  onChange={(e: any) => setEmail(e.target.value)}
                  placeholder="johndoe@company.com"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Phone Number</label>
                <Input
                  type="tel"
                  value={phone}
                  onChange={(e: any) => setPhone(e.target.value)}
                  placeholder="+91 98765 43210"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Department</label>
                <Input
                  value={department}
                  onChange={(e: any) => setDepartment(e.target.value)}
                  placeholder="e.g. Engineering, HR"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Job Title / Position</label>
                <Input
                  value={position}
                  onChange={(e: any) => setPosition(e.target.value)}
                  placeholder="e.g. Software Engineer"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Office Location</label>
                <Input
                  value={location}
                  onChange={(e: any) => setLocation(e.target.value)}
                  placeholder="e.g. Bangalore, Remote"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Date of Joining</label>
                <Input
                  type="date"
                  value={joiningDate}
                  onChange={(e: any) => setJoiningDate(e.target.value)}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-end gap-3">
          <Link href="/admin/employees" passHref>
            <Button type="button" variant="outline" className="border-border">
              Cancel
            </Button>
          </Link>
          <Button type="submit" className="bg-primary hover:bg-primary/90 text-white min-w-[150px]" disabled={loading}>
            {loading ? "Generating account..." : "Create Employee"}
          </Button>
        </div>
      </form>
    </div>
  );
}
