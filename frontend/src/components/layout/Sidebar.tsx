"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Users, 
  Clock, 
  Calendar, 
  UserCircle,
  LayoutDashboard,
  Wallet
} from "lucide-react";
import { cn } from "../../lib/utils";
import { useEffect, useState } from "react";
import { authService } from "../../services/auth";
import type { Employee } from "../../data/mockData";

export function Sidebar() {
  const pathname = usePathname();
  const [user, setUser] = useState<Employee | null>(null);

  useEffect(() => {
    setUser(authService.getCurrentUser());
  }, []);

  const employeeLinks = [
    { href: "/employee", label: "Dashboard", icon: LayoutDashboard },
    { href: "/employee/profile", label: "My Profile", icon: UserCircle },
    { href: "/employee/attendance", label: "Attendance", icon: Clock },
    { href: "/employee/time-off", label: "Time Off", icon: Calendar },
  ];

  const adminLinks = [
    { href: "/admin", label: "Dashboard", icon: LayoutDashboard },
    { href: "/admin/employees", label: "Employees", icon: Users },
    { href: "/admin/attendance", label: "Attendance", icon: Clock },
    { href: "/admin/time-off", label: "Time Off", icon: Calendar },
  ];

  const links = user?.role === "EMPLOYEE" ? employeeLinks : adminLinks;

  if (!user) return null;

  return (
    <aside className="w-64 border-r bg-sidebar h-[calc(100vh-4rem)] sticky top-16 hidden md:block shrink-0">
      <div className="p-4 py-6 flex flex-col gap-2">
        <div className="mb-4 px-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          Main Menu
        </div>
        {links.map((link) => {
          const isActive = pathname === link.href || (pathname.startsWith(link.href) && link.href !== "/admin" && link.href !== "/employee");
          
          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive 
                  ? "bg-primary/10 text-primary" 
                  : "text-foreground hover:bg-muted"
              )}
            >
              <link.icon className={cn("h-4 w-4", isActive ? "text-primary" : "text-muted-foreground")} />
              {link.label}
            </Link>
          );
        })}
      </div>
    </aside>
  );
}
