import { timeOffRequests, TimeOffRequest } from "../data/mockData";

let requests = [...timeOffRequests];

export const timeoffService = {
  getByEmployee: async (employeeId: string): Promise<TimeOffRequest[]> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return requests.filter(r => r.employeeId === employeeId);
  },

  getAll: async (): Promise<TimeOffRequest[]> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return requests;
  },

  create: async (request: Omit<TimeOffRequest, "id" | "status">): Promise<TimeOffRequest> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const newReq: TimeOffRequest = {
      ...request,
      id: `to_${Date.now()}`,
      status: "Pending"
    };
    requests = [newReq, ...requests];
    return newReq;
  },

  updateStatus: async (requestId: string, status: "Approved" | "Rejected"): Promise<TimeOffRequest | null> => {
    await new Promise(resolve => setTimeout(resolve, 500));
    const reqIndex = requests.findIndex(r => r.id === requestId);
    if (reqIndex === -1) return null;
    
    requests[reqIndex] = { ...requests[reqIndex], status };
    return requests[reqIndex];
  }
};
