"use client";

import { useEffect, useState } from "react";
import { employeesService } from "@/services/employees";
import { Employee } from "@/data/mockData";
import { EmployeeCard } from "@/components/shared/EmployeeCard";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, Plus } from "lucide-react";
import { authService } from "@/services/auth";
import Link from "next/link";

export default function AdminEmployeesPage() {
  const [employeesList, setEmployeesList] = useState<Employee[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmployees = async () => {
      const data = await employeesService.getAll();
      setEmployeesList(data);
      setLoading(false);
    };
    fetchEmployees();
  }, []);

  const filteredEmployees = employeesList.filter(e => 
    e.name.toLowerCase().includes(search.toLowerCase()) || 
    e.department.toLowerCase().includes(search.toLowerCase()) ||
    e.position.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Employees</h2>
          <p className="text-muted-foreground mt-1">Manage your workforce, view profiles, and track statuses.</p>
        </div>
        <Link href="/admin/employees/new" passHref legacyBehavior>
          <Button className="bg-primary hover:bg-primary/90 text-white gap-2 shadow-sm">
            <Plus className="w-4 h-4" />
            New Employee
          </Button>
        </Link>
      </div>

      <div className="flex items-center gap-2 max-w-sm">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search employees..."
            className="pl-8 bg-white border-border"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-48 rounded-lg bg-gray-100 animate-pulse border border-border"></div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredEmployees.map(employee => (
            <EmployeeCard 
              key={employee.id} 
              employee={employee} 
              href={`/admin/employees/${employee.id}`} 
            />
          ))}
        </div>
      )}
    </div>
  );
}
