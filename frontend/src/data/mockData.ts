export type Role = "EMPLOYEE" | "ADMIN" | "HR_OFFICER";

export interface Employee {
  id: string;
  loginId: string;
  name: string;
  role: Role;
  avatar: string;
  email: string;
  phone: string;
  department: string;
  position: string;
  location: string;
  manager: string;
  joiningDate: string;
  status: "GREEN" | "BLUE" | "YELLOW";
  
  // Auth
  password: string;
  firstLogin: boolean;
  
  // Private Info
  dateOfBirth?: string;
  residingAddress?: string;
  nationality?: string;
  personalEmail?: string;
  gender?: string;
  maritalStatus?: string;
  
  // Bank Details
  accountNumber?: string;
  bankName?: string;
  ifscCode?: string;
  panNo?: string;
  uanNo?: string;
}

export interface AttendanceRecord {
  id: string;
  employeeId: string;
  date: string;
  checkIn: string;
  checkOut: string | null;
  workHours: number;
  extraHours: number;
}

export interface TimeOffRequest {
  id: string;
  employeeId: string;
  type: "Paid Time Off" | "Sick Leave" | "Unpaid Leave";
  startDate: string;
  endDate: string;
  days: number;
  status: "Pending" | "Approved" | "Rejected";
}

export interface SalaryComponent {
  id: string;
  name: string;
  type: "PERCENTAGE" | "FIXED";
  value: number; // percentage or fixed amount
}

export interface SalaryInfo {
  employeeId: string;
  monthWage: number;
  yearlyWage: number;
  workingDays: number;
  workingSchedule: string;
  breakTime: string;
  wageType: string;
  components: SalaryComponent[];
  pfRate: number; // percentage
  professionalTax: number;
}

// Initial mock data
export const employees: Employee[] = [
  {
    id: "emp_1",
    loginId: "OIAA20230001",
    name: "Aarav Sharma",
    role: "ADMIN",
    avatar: "https://i.pravatar.cc/150?u=Aarav",
    email: "aarav.sharma@dayflow.com",
    phone: "+91 9876543210",
    department: "Engineering",
    position: "Lead Engineer",
    location: "Bangalore",
    manager: "Karthik Raj",
    joiningDate: "2023-01-15",
    status: "GREEN",
    dateOfBirth: "1990-05-20",
    residingAddress: "123 Tech Park, Bangalore",
    nationality: "Indian",
    personalEmail: "aarav.personal@email.com",
    gender: "Male",
    maritalStatus: "Single",
    password: "password123",
    firstLogin: false
  },
  {
    id: "emp_2",
    loginId: "OIPK20230002",
    name: "Priya Kumar",
    role: "HR_OFFICER",
    avatar: "https://i.pravatar.cc/150?u=Priya",
    email: "priya.kumar@dayflow.com",
    phone: "+91 9876543211",
    department: "Human Resources",
    position: "HR Manager",
    location: "Mumbai",
    manager: "Aarav Sharma",
    joiningDate: "2023-02-01",
    status: "BLUE",
    password: "password123",
    firstLogin: false
  },
  {
    id: "emp_3",
    loginId: "OIRS20230003",
    name: "Rahul Singh",
    role: "EMPLOYEE",
    avatar: "https://i.pravatar.cc/150?u=Rahul",
    email: "rahul.singh@dayflow.com",
    phone: "+91 9876543212",
    department: "Marketing",
    position: "Marketing Specialist",
    location: "Delhi",
    manager: "Priya Kumar",
    joiningDate: "2023-03-10",
    status: "YELLOW",
    password: "password123",
    firstLogin: true
  },
  {
    id: "emp_4",
    loginId: "OIAA20230004",
    name: "Ananya Patel",
    role: "EMPLOYEE",
    avatar: "https://i.pravatar.cc/150?u=Ananya",
    email: "ananya.patel@dayflow.com",
    phone: "+91 9876543213",
    department: "Design",
    position: "UI/UX Designer",
    location: "Pune",
    manager: "Aarav Sharma",
    joiningDate: "2023-04-15",
    status: "GREEN",
    password: "password123",
    firstLogin: false
  },
  {
    id: "emp_5",
    loginId: "OIKR20230005",
    name: "Karthik Raj",
    role: "ADMIN",
    avatar: "https://i.pravatar.cc/150?u=Karthik",
    email: "karthik.raj@dayflow.com",
    phone: "+91 9876543214",
    department: "Executive",
    position: "CEO",
    location: "Bangalore",
    manager: "N/A",
    joiningDate: "2022-01-01",
    status: "GREEN",
    password: "password123",
    firstLogin: false
  }
];

export const attendanceRecords: AttendanceRecord[] = [
  {
    id: "att_1",
    employeeId: "emp_3",
    date: "2023-10-01",
    checkIn: "09:00",
    checkOut: "17:30",
    workHours: 8.5,
    extraHours: 0
  },
  {
    id: "att_2",
    employeeId: "emp_3",
    date: "2023-10-02",
    checkIn: "09:15",
    checkOut: "18:00",
    workHours: 8.75,
    extraHours: 0.75
  }
];

export const timeOffRequests: TimeOffRequest[] = [
  {
    id: "to_1",
    employeeId: "emp_3",
    type: "Paid Time Off",
    startDate: "2023-10-15",
    endDate: "2023-10-16",
    days: 2,
    status: "Pending"
  },
  {
    id: "to_2",
    employeeId: "emp_4",
    type: "Sick Leave",
    startDate: "2023-10-05",
    endDate: "2023-10-06",
    days: 2,
    status: "Approved"
  }
];

export const salaryInfos: SalaryInfo[] = [
  {
    employeeId: "emp_3",
    monthWage: 50000,
    yearlyWage: 600000,
    workingDays: 22,
    workingSchedule: "Mon-Fri",
    breakTime: "1 Hour",
    wageType: "Fixed wage",
    pfRate: 12,
    professionalTax: 200,
    components: [
      { id: "c1", name: "Basic Salary", type: "PERCENTAGE", value: 50 },
      { id: "c2", name: "House Rent Allowance", type: "PERCENTAGE", value: 25 },
      { id: "c3", name: "Fixed Allowance", type: "FIXED", value: 12500 }
    ]
  }
];
