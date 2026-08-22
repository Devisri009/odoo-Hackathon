"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Employee, employeesService } from "../../../../../../services/employees";
import { authService } from "../../../../../../services/auth";
import { payrollService } from "../../../../../../services/payroll";
import type { SalaryInfo, SalaryComponent } from "../../../../../../data/mockData";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "../../../../../../components/ui/card";
import { Button } from "../../../../../../components/ui/button";
import { Input } from "../../../../../../components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../../../../../components/ui/select";
import { ArrowLeft, Plus, Save, Trash2 } from "lucide-react";
import { toast } from "sonner";

export default function AdminEmployeeSalaryPage() {
  const params = useParams();
  const router = useRouter();
  
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [salaryInfo, setSalaryInfo] = useState<SalaryInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const user = authService.getCurrentUser();
    if (user?.role !== "ADMIN") {
      router.push("/login");
      return;
    }

    const loadData = async () => {
      const empId = params.id as string;
      const emp = await employeesService.getById(empId);
      if (emp) {
        setEmployee(emp);
        let info = await payrollService.getByEmployee(empId);
        if (!info) {
          info = await payrollService.updateSalaryInfo(empId, {});
        }
        setSalaryInfo(info);
      }
      setLoading(false);
    };
    loadData();
  }, [params.id, router]);

  if (loading || !salaryInfo || !employee) {
    return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading salary configuration...</div>;
  }

  const handleUpdateBase = (field: keyof SalaryInfo, value: any) => {
    setSalaryInfo(prev => prev ? { ...prev, [field]: value } : null);
  };

  const addComponent = () => {
    const newComponent: SalaryComponent = {
      id: `c_${Date.now()}`,
      name: "New Component",
      type: "PERCENTAGE",
      value: 0
    };
    setSalaryInfo(prev => prev ? {
      ...prev,
      components: [...prev.components, newComponent]
    } : null);
  };

  const updateComponent = (id: string, field: keyof SalaryComponent, value: any) => {
    setSalaryInfo(prev => prev ? {
      ...prev,
      components: prev.components.map(c => c.id === id ? { ...c, [field]: value } : c)
    } : null);
  };

  const removeComponent = (id: string) => {
    setSalaryInfo(prev => prev ? {
      ...prev,
      components: prev.components.filter(c => c.id !== id)
    } : null);
  };

  const handleSave = async () => {
    setSaving(true);
    await payrollService.updateSalaryInfo(employee.id, salaryInfo);
    toast.success("Salary Info Saved", { description: "Configuration has been updated successfully." });
    setSaving(false);
  };

  const totals = payrollService.calculateTotalSalary(salaryInfo);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={() => router.back()} className="h-8 w-8">
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h2 className="text-2xl font-bold">Salary Configuration</h2>
            <p className="text-muted-foreground text-sm">{employee.name} - {employee.position}</p>
          </div>
        </div>
        <Button onClick={handleSave} disabled={saving} className="bg-primary hover:bg-primary/90 text-white gap-2">
          <Save className="w-4 h-4" />
          {saving ? "Saving..." : "Save Changes"}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card className="shadow-sm">
            <CardHeader>
              <CardTitle>Base Information</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Monthly Wage (₹)</label>
                <Input 
                  type="number" 
                  value={salaryInfo.monthWage} 
                  onChange={e => handleUpdateBase("monthWage", parseFloat(e.target.value) || 0)} 
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Yearly Wage (₹)</label>
                <Input 
                  type="number" 
                  value={salaryInfo.monthWage * 12} 
                  disabled
                  className="bg-gray-50"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Wage Type</label>
                <Select value={salaryInfo.wageType} onValueChange={(val) => handleUpdateBase("wageType", val)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Fixed wage">Fixed wage</SelectItem>
                    <SelectItem value="Hourly">Hourly</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Working Days / Month</label>
                <Input 
                  type="number" 
                  value={salaryInfo.workingDays} 
                  onChange={e => handleUpdateBase("workingDays", parseInt(e.target.value) || 0)} 
                />
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-sm">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Salary Components</CardTitle>
              <Button variant="outline" size="sm" onClick={addComponent} className="gap-2">
                <Plus className="w-3.5 h-3.5" /> Add
              </Button>
            </CardHeader>
            <CardContent className="space-y-4">
              {salaryInfo.components.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">No components defined.</p>
              ) : (
                salaryInfo.components.map(comp => (
                  <div key={comp.id} className="flex flex-wrap sm:flex-nowrap items-end gap-3 p-3 border rounded-md bg-gray-50/50">
                    <div className="w-full sm:w-2/5 space-y-1.5">
                      <label className="text-xs font-medium text-muted-foreground">Name</label>
                      <Input 
                        value={comp.name} 
                        onChange={e => updateComponent(comp.id, "name", e.target.value)} 
                        className="bg-white"
                      />
                    </div>
                    <div className="w-full sm:w-1/4 space-y-1.5">
                      <label className="text-xs font-medium text-muted-foreground">Type</label>
                      <Select value={comp.type} onValueChange={(val) => updateComponent(comp.id, "type", val)}>
                        <SelectTrigger className="bg-white">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="PERCENTAGE">Percentage (%)</SelectItem>
                          <SelectItem value="FIXED">Fixed Amount (₹)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="w-full sm:w-1/4 space-y-1.5">
                      <label className="text-xs font-medium text-muted-foreground">Value</label>
                      <Input 
                        type="number" 
                        value={comp.value} 
                        onChange={e => updateComponent(comp.id, "value", parseFloat(e.target.value) || 0)} 
                        className="bg-white"
                      />
                    </div>
                    <Button variant="ghost" size="icon" onClick={() => removeComponent(comp.id)} className="text-destructive hover:bg-destructive/10 shrink-0">
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                ))
              )}
            </CardContent>
          </Card>

          <Card className="shadow-sm">
            <CardHeader>
              <CardTitle>Deductions</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">PF Rate (%)</label>
                <Input 
                  type="number" 
                  value={salaryInfo.pfRate} 
                  onChange={e => handleUpdateBase("pfRate", parseFloat(e.target.value) || 0)} 
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Professional Tax (₹)</label>
                <Input 
                  type="number" 
                  value={salaryInfo.professionalTax} 
                  onChange={e => handleUpdateBase("professionalTax", parseFloat(e.target.value) || 0)} 
                />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-1">
          <Card className="shadow-sm sticky top-24 border-primary/20">
            <CardHeader className="bg-primary/5 pb-4">
              <CardTitle>Calculation Preview</CardTitle>
              <CardDescription>Automatic breakdown</CardDescription>
            </CardHeader>
            <CardContent className="pt-6 space-y-4">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Base Wage</span>
                <span className="font-medium">₹{salaryInfo.monthWage.toFixed(2)}</span>
              </div>
              
              <div className="space-y-2 py-3 border-y">
                <p className="text-xs font-semibold text-muted-foreground uppercase">Earnings</p>
                {salaryInfo.components.map(comp => {
                  const val = payrollService.calculateComponentValue(salaryInfo.monthWage, comp);
                  return (
                    <div key={comp.id} className="flex justify-between items-center text-sm">
                      <span className="text-muted-foreground">{comp.name} {comp.type === "PERCENTAGE" && `(${comp.value}%)`}</span>
                      <span className="font-medium text-green-700">+ ₹{val.toFixed(2)}</span>
                    </div>
                  );
                })}
              </div>

              <div className="space-y-2 py-3 border-b">
                <p className="text-xs font-semibold text-muted-foreground uppercase">Deductions</p>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Provident Fund ({salaryInfo.pfRate}%)</span>
                  <span className="font-medium text-destructive">- ₹{((salaryInfo.monthWage * salaryInfo.pfRate) / 100).toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground">Professional Tax</span>
                  <span className="font-medium text-destructive">- ₹{salaryInfo.professionalTax.toFixed(2)}</span>
                </div>
              </div>

              <div className="pt-2 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-semibold">Gross Salary</span>
                  <span className="font-bold">₹{totals.gross.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-semibold">Total Deductions</span>
                  <span className="font-bold text-destructive">₹{totals.deductions.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-secondary/10 rounded-md border border-secondary/20">
                  <span className="font-bold text-lg text-primary">Net Payable</span>
                  <span className="font-bold text-lg text-primary">₹{totals.net.toFixed(2)}</span>
                </div>
              </div>
              
              {totals.gross > salaryInfo.monthWage && (
                <div className="p-3 bg-yellow-50 text-yellow-800 text-sm rounded border border-yellow-200 mt-4">
                  Warning: Total components (₹{totals.gross.toFixed(2)}) exceed the defined base wage (₹{salaryInfo.monthWage}).
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
