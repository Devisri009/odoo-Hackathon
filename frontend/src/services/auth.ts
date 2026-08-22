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
  
  validateLoginId: (loginId: string): boolean => {
    // Format: [2 letters] + [4 letters] + [4 digits year] + [4 digits serial]
    const regex = /^[A-Z]{2}[A-Z]{4}\d{4}\d{4}$/;
    return regex.test(loginId);
  }
};

