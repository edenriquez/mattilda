-- DropForeignKey
ALTER TABLE "students" DROP CONSTRAINT "students_schoolId_fkey";

-- AddForeignKey
ALTER TABLE "students" ADD CONSTRAINT "students_schoolId_fkey" FOREIGN KEY ("schoolId") REFERENCES "schools"("id") ON DELETE CASCADE ON UPDATE CASCADE;
