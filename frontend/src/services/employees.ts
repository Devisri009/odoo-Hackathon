import { Employee } from "../data/mockData";
import { getActiveEmployees, saveEmployees } from "./auth";

export const employeesService = {
  getAll: async (): Promise<Employee[]> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return getActiveEmployees();
  },

  getById: async (id: string): Promise<Employee | undefined> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return getActiveEmployees().find(e => e.id === id);
  },

  createEmployee: async (data: {
    name: string;
    email: string;
    phone: string;
    companyName: string;
    role: "EMPLOYEE" | "HR_OFFICER" | "ADMIN";
    department: string;
    position: string;
    location: string;
    joiningDate?: string;
  }): Promise<{ employee: Employee; loginId: string; tempPassword: string }> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const list = getActiveEmployees();

    // 1. Company Code: 2 letters uppercase
    const companyCode = (data.companyName.replace(/[^a-zA-Z]/g, "").substring(0, 2) || "OI").toUpperCase();

    // 2. Name Code: first 2 letters of first and last name
    const nameParts = data.name.trim().split(/\s+/);
    let nameCode = "";
    if (nameParts.length >= 2) {
      nameCode = (nameParts[0].substring(0, 2) + nameParts[nameParts.length - 1].substring(0, 2)).toUpperCase();
    } else if (nameParts.length === 1) {
      nameCode = (nameParts[0].substring(0, 4).padEnd(4, "X")).toUpperCase();
    } else {
      nameCode = "XXXX";
    }

    // 3. Joining Year
    const joiningDate = data.joiningDate || new Date().toISOString().split("T")[0];
    const joiningYear = new Date(joiningDate).getFullYear().toString();

    // 4. Joining Serial: based on year
    const sameYearEmployees = list.filter(e => {
      // loginId index mapping: Co(2) Name(4) Year(4) Serial(4)
      if (e.loginId && e.loginId.length >= 10) {
        const yearPart = e.loginId.substring(6, 10);
        return yearPart === joiningYear;
      }
      return false;
    });

    const nextSerialNum = sameYearEmployees.length + 1;
    const serialStr = nextSerialNum.toString().padStart(4, "0");

    const loginId = `${companyCode}${nameCode}${joiningYear}${serialStr}`;
    const tempPassword = Math.random().toString(36).substring(2, 10).toUpperCase(); // 8 char uppercase alphanumeric-like

    const newEmployee: Employee = {
      id: `emp_${list.length + 1}`,
      loginId,
      name: data.name,
      role: data.role,
      avatar: `https://i.pravatar.cc/150?u=${encodeURIComponent(data.name)}`,
      email: data.email,
      phone: data.phone,
      department: data.department,
      position: data.position,
      location: data.location,
      manager: "Aarav Sharma",
      joiningDate,
      status: "GREEN",
      password: tempPassword,
      firstLogin: true
    };

    list.push(newEmployee);
    saveEmployees(list);

    return {
      employee: newEmployee,
      loginId,
      tempPassword
    };
  }
};

