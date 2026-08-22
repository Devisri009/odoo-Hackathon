"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { authService } from "../../../services/auth";
import { Button } from "../../../components/ui/button";
import { Input } from "../../../components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "../../../components/ui/card";
import { toast } from "sonner";
import { Eye, EyeOff } from "lucide-react";

export default function LoginPage() {
  const [loginId, setLoginId] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const identifier = loginId.trim();
    const isEmail = identifier.includes("@");

    if (!isEmail && !authService.validateLoginId(identifier.toUpperCase())) {
      toast.error("Invalid Format", {
        description: "Must be a valid email or Login ID format (e.g. OIAA20230001).",
      });
      setLoading(false);
      return;
    }

    const user = await authService.login(identifier, password);
    setLoading(false);

    if (user) {
      toast.success("Login Successful", {
        description: `Welcome back, ${user.name}!`,
      });
      
      if (user.firstLogin) {
        router.push("/change-password");
      } else if (user.role === "EMPLOYEE") {
        router.push("/employee");
      } else {
        router.push("/admin");
      }
    } else {
      toast.error("Login Failed", {
        description: "Invalid credentials.",
      });
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4 animate-fade-in">
      <Card className="w-full max-w-md border-border shadow-sm">
        <CardHeader className="text-center space-y-2">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-primary rounded flex items-center justify-center">
              <span className="text-white font-bold text-xl">D</span>
            </div>
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight text-foreground">DAYFLOW</CardTitle>
          <CardDescription className="text-sm text-muted-foreground">Every workday, perfectly aligned.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Login ID / Email</label>
              <Input
                placeholder="e.g. OIAA20230001 or email@domain.com"
                value={loginId}
                onChange={(e) => setLoginId(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Password</label>
              <div className="relative">
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            <Button type="submit" className="w-full bg-primary hover:bg-primary/90 text-white" disabled={loading}>
              {loading ? "Signing in..." : "Sign In"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center border-t pt-4">
          <p className="text-sm text-muted-foreground text-center">
            Employee accounts are created by HR. <br/>
            Contact Admin if you don't have access.
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}

