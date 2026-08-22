import Link from "next/link";
import { Employee } from "../../data/mockData";
import { Card, CardContent } from "../ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { StatusBadge } from "./StatusBadge";
import { Briefcase, MapPin, Mail, Phone } from "lucide-react";

export function EmployeeCard({ employee, href }: { employee: Employee; href?: string }) {
  const cardContent = (
    <Card className="overflow-hidden hover:border-primary/50 transition-colors shadow-sm h-full">
      <CardContent className="p-5 flex flex-col gap-4">
        <div className="flex justify-between items-start">
          <Avatar className="h-14 w-14 border border-border">
            <AvatarImage src={employee.avatar} alt={employee.name} />
            <AvatarFallback className="bg-primary/10 text-primary text-lg font-medium">{employee.name.charAt(0)}</AvatarFallback>
          </Avatar>
          <StatusBadge status={employee.status} />
        </div>
        
        <div>
          <h3 className="font-semibold text-lg text-foreground">{employee.name}</h3>
          <p className="text-sm text-muted-foreground flex items-center gap-1.5 mt-1">
            <Briefcase className="w-3.5 h-3.5" />
            {employee.position}
          </p>
        </div>
        
        <div className="space-y-2 mt-2 pt-4 border-t text-sm">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Mail className="w-3.5 h-3.5" />
            <span className="truncate">{employee.email}</span>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground">
            <Phone className="w-3.5 h-3.5" />
            <span>{employee.phone}</span>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground">
            <MapPin className="w-3.5 h-3.5" />
            <span>{employee.location}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  if (href) {
    return (
      <Link href={href} className="block outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 rounded-lg h-full">
        {cardContent}
      </Link>
    );
  }

  return cardContent;
}
