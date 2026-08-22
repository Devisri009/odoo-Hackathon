"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { toast } from "sonner";
import { Eye, EyeOff, Upload, X, Check, Copy } from "lucide-react";
import Link from "next/link";

export default function SignUpPage() {
  const [companyName, setCompanyName] = useState("");
  const [companyLogo, setCompanyLogo] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [createdCredentials, setCreatedCredentials] = useState<{ loginId: string } | null>(null);
  const [copiedLoginId, setCopiedLoginId] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const handleLogoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setCompanyLogo(reader.result as string);
        toast.success("Logo uploaded successfully");
      };
      reader.readAsDataURL(file);
    }
  };

  const removeLogo = () => {
    setCompanyLogo(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const validateEmail = (emailStr: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailStr);
  };

  const validatePhone = (phoneStr: string) => {
    // Basic phone validation (allowing digits, spaces, hyphens, and optional +)
    return /^\+?[\d\s-]{8,15}$/.test(phoneStr);
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!companyName.trim() || !name.trim() || !email.trim() || !phone.trim() || !password || !confirmPassword) {
      toast.error("Validation Error", {
        description: "Please fill out all required fields.",
      });
      return;
    }

    if (!validateEmail(email.trim())) {
      toast.error("Validation Error", {
        description: "Please enter a valid email address.",
      });
      return;
    }

    if (!validatePhone(phone.trim())) {
      toast.error("Validation Error", {
        description: "Please enter a valid phone number.",
      });
      return;
    }

    if (password.length < 8) {
      toast.error("Validation Error", {
        description: "Password must be at least 8 characters long.",
      });
      return;
    }

    if (password !== confirmPassword) {
      toast.error("Validation Error", {
        description: "Passwords do not match.",
      });
      return;
    }

    setLoading(true);

    try {
      const result = await authService.register({
        companyName: companyName.trim(),
        companyLogo,
        name: name.trim(),
        email: email.trim(),
        phone: phone.trim(),
        password,
      });

      setCreatedCredentials({
        loginId: result.loginId,
      });

      toast.success("Account Created Successfully!");
    } catch (err) {
      toast.error("Registration Failed", {
        description: "An error occurred during sign up. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, type: "login") => {
    navigator.clipboard.writeText(text);
    if (type === "login") {
      setCopiedLoginId(true);
      setTimeout(() => setCopiedLoginId(false), 2000);
    }
    toast.success("Copied to clipboard!");
  };

  if (createdCredentials) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4 animate-fade-in">
        <Card className="w-full max-w-md border-border shadow-sm bg-emerald-50/20 border-emerald-100">
          <CardHeader className="text-center pb-2">
            <div className="flex justify-center mb-2 text-emerald-600">
              <Check size={48} className="animate-bounce" />
            </div>
            <CardTitle className="text-2xl font-bold text-emerald-800">Account Created!</CardTitle>
            <CardDescription className="text-emerald-700">
              Welcome to Dayflow. Credentials generated for {name}.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6 pt-4">
            <div className="bg-white p-4 rounded-lg border border-emerald-100 shadow-sm space-y-4">
              <div className="space-y-1">
                <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider block">Your Login ID</span>
                <div className="flex items-center justify-between bg-gray-50 p-2.5 rounded border border-gray-200">
                  <code className="font-mono text-base font-bold text-gray-800">{createdCredentials.loginId}</code>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-8 w-8 p-0 hover:bg-emerald-100/50 hover:text-emerald-700"
                    onClick={() => copyToClipboard(createdCredentials.loginId, "login")}
                  >
                    {copiedLoginId ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4 text-gray-500" />}
                  </Button>
                </div>
              </div>

              <div className="space-y-1">
                <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider block">Password</span>
                <div className="bg-gray-50 p-2.5 rounded border border-gray-200">
                  <span className="text-sm font-medium text-gray-600">•••••••• (Your chosen password)</span>
                </div>
              </div>
            </div>

            <div className="text-center space-y-4 pt-2">
              <p className="text-sm text-emerald-800">
                Please save your **Login ID** securely. You must use this ID to sign in.
              </p>
              <Link href="/login" passHref className="block w-full">
                <Button className="w-full bg-primary hover:bg-primary/90 text-white">
                  Proceed to Sign In
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

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
          <form onSubmit={handleSignUp} className="space-y-4">
            {/* Company Details Row (Name + Upload Side-by-Side) */}
            <div className="grid grid-cols-[1fr_auto] gap-3 items-end">
              <div className="space-y-2">
                <label className="text-sm font-medium">Company Name</label>
                <Input
                  placeholder="e.g. Odoo India"
                  value={companyName}
                  onChange={(e: any) => setCompanyName(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium block">Company Logo</label>
                <div className="flex items-center gap-2">
                  {companyLogo ? (
                    <div className="relative w-8 h-8 border rounded bg-white overflow-hidden flex items-center justify-center">
                      <img src={companyLogo} alt="Logo Preview" className="max-w-full max-h-full object-contain" />
                      <button
                        type="button"
                        onClick={removeLogo}
                        className="absolute top-0 right-0 bg-red-500 hover:bg-red-600 text-white rounded-full p-0.5 shadow-sm"
                      >
                        <X className="w-2.5 h-2.5" />
                      </button>
                    </div>
                  ) : (
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => fileInputRef.current?.click()}
                      className="h-8 px-2 flex items-center justify-center border-dashed border-gray-300 gap-1"
                    >
                      <Upload className="w-3.5 h-3.5 text-muted-foreground" />
                      <span className="text-xs">Upload</span>
                    </Button>
                  )}
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleLogoUpload}
                    accept="image/*"
                    className="hidden"
                  />
                </div>
              </div>
            </div>

            {/* Name */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Name</label>
              <Input
                placeholder="e.g. John Doe"
                value={name}
                onChange={(e: any) => setName(e.target.value)}
                required
              />
            </div>

            {/* Email */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Email</label>
              <Input
                type="email"
                placeholder="email@domain.com"
                value={email}
                onChange={(e: any) => setEmail(e.target.value)}
                required
              />
            </div>

            {/* Phone */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Phone</label>
              <Input
                type="tel"
                placeholder="e.g. +91 98765 43210"
                value={phone}
                onChange={(e: any) => setPhone(e.target.value)}
                required
              />
            </div>

            {/* Password */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Password</label>
              <div className="relative">
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e: any) => setPassword(e.target.value)}
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

            {/* Confirm Password */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Confirm Password</label>
              <div className="relative">
                <Input
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e: any) => setConfirmPassword(e.target.value)}
                  required
                  className="pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
                >
                  {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* Sign Up Button */}
            <Button
              type="submit"
              className="w-full bg-primary hover:bg-primary/90 text-white mt-2"
              disabled={loading}
            >
              {loading ? "Signing up..." : "Sign Up"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center border-t pt-4">
          <p className="text-sm text-muted-foreground text-center">
            Already have an account?{" "}
            <Link href="/login" className="text-primary hover:underline font-medium">
              Sign In
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}
