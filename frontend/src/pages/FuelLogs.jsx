import ManagementPage from '../components/pages/ManagementPage';
import { managementConfigs } from '../config/entityConfigs';

export default function FuelLogs() {
  return <ManagementPage config={managementConfigs.fuelLogs} />;
}