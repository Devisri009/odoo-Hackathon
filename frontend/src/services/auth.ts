import { employees as initialEmployees, Employee } from "../data/mockData";

export const getActiveEmployees = (): Employee[] => {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem("dayflow_employees");
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch (e) {
        console.error(e);
      }
    }
  }
  return initialEmployees;
};

export const saveEmployees = (list: Employee[]) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem("dayflow_employees", JSON.stringify(list));
  }
};

let currentUser: Employee | null = null;

export const authService = {
  login: async (loginIdOrEmail: string, password?: string): Promise<Employee | null> => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));
    const list = getActiveEmployees();
    const user = list.find(e => 
      (e.loginId.toLowerCase() === loginIdOrEmail.toLowerCase() || 
       e.email.toLowerCase() === loginIdOrEmail.toLowerCase()) &&
      e.password === password
    );
    if (user) {
      currentUser = user;
      // In a real app, we'd store a token in localStorage/cookies
      if (typeof window !== 'undefined') {
        localStorage.setItem("currentUser", JSON.stringify(user));
      }
      return user;
    }
    return null;
  },

  changePassword: async (employeeId: string, newPassword: string): Promise<boolean> => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500));
    const list = getActiveEmployees();
    const index = list.findIndex(e => e.id === employeeId);
    if (index !== -1) {
      list[index].password = newPassword;
      list[index].firstLogin = false;
      saveEmployees(list);
      
      // Also update currentUser if it's the logged-in user
      if (currentUser && currentUser.id === employeeId) {
        currentUser = list[index];
        if (typeof window !== 'undefined') {
          localStorage.setItem("currentUser", JSON.stringify(currentUser));
        }
      }
      return true;
    }
    return false;
  },

  getCurrentUser: (): Employee | null => {
    if (currentUser) return currentUser;
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem("currentUser");
      if (stored) {
        currentUser = JSON.parse(stored);
        return currentUser;
      }
    }
    return null;
  },

  logout: () => {
    currentUser = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem("currentUser");
    }
  },
  
  register: async (data: {
    companyName: string;
    companyLogo?: string | null;
    name: string;
    email: string;
    phone: string;
    password: string;
  }): Promise<{ employee: Employee; loginId: string }> => {
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
    const joiningDate = new Date().toISOString().split("T")[0];
    const joiningYear = new Date(joiningDate).getFullYear().toString();

    // 4. Joining Serial: based on year
    const sameYearEmployees = list.filter(e => {
      if (e.loginId && e.loginId.length >= 10) {
        const yearPart = e.loginId.substring(6, 10);
        return yearPart === joiningYear;
      }
      return false;
    });

    const nextSerialNum = sameYearEmployees.length + 1;
    const serialStr = nextSerialNum.toString().padStart(4, "0");

    const loginId = `${companyCode}${nameCode}${joiningYear}${serialStr}`;

    const newEmployee: Employee = {
      id: `emp_${list.length + 1}`,
      loginId,
      name: data.name,
      role: "EMPLOYEE",
      avatar: data.companyLogo || `https://i.pravatar.cc/150?u=${encodeURIComponent(data.name)}`,
      email: data.email,
      phone: data.phone,
      department: "General",
      position: "New Hire",
      location: "Remote",
      manager: "Aarav Sharma",
      joiningDate,
      status: "GREEN",
      password: data.password,
      firstLogin: false
    };

    list.push(newEmployee);
    saveEmployees(list);

    return {
      employee: newEmployee,
      loginId
    };
  },
  
  validateLoginId: (loginId: string): boolean => {
    // Format: [2 letters] + [4 letters] + [4 digits year] + [4 digits serial]
    const regex = /^[A-Z]{2}[A-Z]{4}\d{4}\d{4}$/;
    return regex.test(loginId);
  }
};

