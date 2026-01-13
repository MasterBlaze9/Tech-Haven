# Factory Manager - Complete Initialization Flow

## 📋 What Happens When You Run `docker-compose up --build`

### Automated Initialization Sequence

When you run `docker-compose up --build`, the following happens **automatically**:

---

## 🗄️ Phase 1: Database Initialization (`init_database.sh`)

### [Step 1/7] Wait for PostgreSQL
- Container waits until PostgreSQL is ready to accept connections
- Ensures database is healthy before proceeding

### [Step 2/7] Create Tables
**Script**: `/sql/create_tables_script_final.sql`

Creates all database tables including:
- ✅ **Warehouse** - Storage locations
- ✅ **Component** - Parts/components  
- ✅ **Supplier** - Suppliers
- ✅ **Supplier_Component** - Supplier-component relationships
- ✅ **Warehouse_Component** - Warehouse inventory
- ✅ **Orders** - Component orders
- ✅ **Order_Component** - Order line items
- ✅ **OrderDelivery** - Delivery records
- ✅ **OrderInvoice** - Invoices
- ✅ **OrderDelivery_Component** - Delivered items
- ✅ **EquipmentType** - Types of equipment
- ✅ **Equipment** - Equipment catalog
- ✅ **WorkType** - Labor types
- ✅ **EquipmentProduction** - Production records
- ✅ **EquipmentProduction_Component** - Components used in production
- ✅ **Client** - Customers
- ✅ **ClientOrder** - Customer orders
- ✅ **ClientOrder_Equipment** - Order line items
- ✅ **ClientOrderDelivery** - Customer deliveries
- ✅ **ClientOrderInvoice** - Customer invoices
- ✅ **ClientOrderDelivery_Equipment** - Delivered equipment

**Total**: ~20 tables with sequences and foreign keys

### [Step 3/7] Import Database Objects
**Location**: `/sql_objects/*/*.sql`

Creates all views, functions, and stored procedures:

#### Views (20):
- viewGetClients
- viewGetSuppliers
- viewGetWarehouses
- viewGetWorkTypes
- viewGetComponents
- viewGetComponentsToOrder
- viewGetEquipments
- viewGetEquipmentsToOrder
- viewGetEquipmentTypes
- viewGetEquipmentProductions
- viewGetOrders
- viewGetOrderComponents
- viewGetClientOrders
- viewGetClientOrderEquipments
- viewGetClientOrderInvoices
- viewGetOrderInvoices
- viewGetWarehouseComponents
- viewGetSuppliersByOrderComponent
- viewGetOrderInvoiceDetails
- viewGetClientOrderInvoiceDetails

#### Functions (~40):
- fnGet[Entity]ById - Retrieve single records
- fnGetLast[Entity]Id - Get latest ID
- fnCalculate[...]Status - Calculate statuses
- fnExportComponents_JSON/XML - Export data
- fnExportOrders_JSON/XML - Export orders
- fnGetOrderComponentsByOrderId - Order details
- fnGetClientOrderEquipmentsByClientOrderId - Order details
- fnTriggerUpdateWarehouseComponentStock - Stock triggers
- fnTriggerUpdateEquipmentProductionComponentStock - Production triggers

#### Stored Procedures (~25):
- spCreateClient, spUpdateClient, spSoftDeleteClient
- spCreateSupplier, spUpdateSupplier, spSoftDeleteSupplier
- spCreateWarehouse, spUpdateWarehouse, spSoftDeleteWarehouse
- spCreateWorkType, spUpdateWorkType, spSoftDeleteWorkType
- spCreateComponent, spUpdateComponent, spSoftDeleteComponent
- spCreateEquipment, spUpdateEquipment, spSoftDeleteEquipment
- spCreateEquipmentType, spUpdateEquipmentType, spSoftDeleteEquipmentType
- spCreateOrder, spCreateOrderComponent
- spCreateOrderDelivery, spCreateOrderDelivery_Component
- spCreateOrderInvoice
- spCreateClientOrder, spCreateClientOrderEquipment
- spCreateClientOrderDelivery, spCreateClientOrderDelivery_Equipment
- spCreateClientOrderInvoice
- spCreateEquipmentProduction, spCreateEquipmentProduction_Component
- spImportComponents_JSON, spImportComponents_XML
- spDeleteSupplierComponentsBySupplierId

### [Step 4/7] Apply Database Privileges
**Script**: `/app/Resources/database_privileges.sql`
- Grants appropriate permissions to database users

### [Step 5/7] Populate Initial Data
**Script**: `/sql/populate_tables.sql`

Inserts initial test data:

✅ **4 Warehouses**:
- Armazém do Norte
- Armazém do Sul  
- Armazém do Este
- Armazém do Oeste

✅ **4 Components**:
- Processador (€500.00)
- RAM (€200.00)
- SSD (€800.00)
- Fonte de Alimentação (€500.00)

✅ **2 Suppliers**:
- Chiptec (NIF: 123456789)
- PcGuia (NIF: 987654321)

✅ **4 Equipment Types**:
- Computador
- Portátil
- Telemóvel
- Tablet

✅ **4 Equipment Items**:
- Computador Desktop (€1000.00)
- Portátil (€800.00)
- Telemóvel (€500.00)
- Tablet (€300.00)

✅ **4 Work Types**:
- Montagem (€100.00)
- Manutenção (€50.00)
- Reparação (€75.00)
- Limpeza (€25.00)

✅ **4 Clients**:
- Cliente 1, 2, 3, 4

✅ **Sample Orders** (3 component orders, 4 client orders)
✅ **Sample Deliveries** with invoices
✅ **Sample Productions** (4 equipment productions)
✅ **Warehouse Stock** initialized

### [Step 6/7] Import Additional Test Data
**Files**: `/sql_objects/*/insert_test_data*.sql`

Currently includes:
- ✅ `insert_test_data_components.sql` - Extra components and suppliers

### [Step 7/7] Verify Setup
- Checks that views were created successfully
- Reports number of views found
- Confirms database initialization complete

---

## 🐍 Phase 2: Django Setup

### Django Migrations
```bash
python3 manage.py migrate
```
- Creates Django's internal tables (auth_user, sessions, etc.)
- Applies any app-specific migrations

### Create Superuser
```bash
python3 manage.py shell < /app/scripts/create_superuser.py
```
- Creates admin user if it doesn't exist
- Default credentials: `admin` / `adminpass`
- Uses ID 1 (matches foreign keys in populate script)

### Seed MongoDB
```bash
python3 /app/scripts/seed_mongo.py
```
- Inserts sample equipment document into MongoDB
- Collection: `equipment`
- Database: `projetofinal`

---

## 🚀 Phase 3: Start Application

### Django Development Server
```bash
python3 manage.py runserver 0.0.0.0:8000
```
- Starts web server on port 8000
- Ready to accept connections

---

## 📊 What You Get After Initialization

### Database Tables: ✅ 20+ tables
All properly structured with:
- Primary keys
- Foreign keys
- Sequences for auto-increment
- Indexes
- Constraints

### Database Objects: ✅ 85+ objects
- 20 Views
- ~40 Functions
- ~25 Stored Procedures

### Sample Data: ✅ Ready to use
- 4 Warehouses with inventory
- 7 Components (4 from populate + 3 from test data)
- 5 Suppliers (2 from populate + 3 from test data)
- 4 Equipment types
- 4 Equipment items
- 4 Work types
- 4 Clients
- 7 Orders (3 component + 4 client)
- Production records
- Deliveries and invoices

### Django: ✅ Configured
- Admin user created
- Migrations applied
- Authentication ready

### MongoDB: ✅ Seeded
- Sample equipment document
- Ready for additional data

---

## 🎯 Summary

**One command does everything:**
```bash
docker-compose up --build
```

**Total initialization time**: ~1-2 minutes

**Result**: Fully functional application with:
- ✅ All tables created
- ✅ All views, functions, procedures installed
- ✅ Sample data loaded (ready to use immediately)
- ✅ Admin user created
- ✅ Application running at http://localhost:8000

**No manual steps required!** 🎉

---

## 🔄 Reset Everything

To start fresh:
```bash
docker-compose down -v  # Remove containers and volumes
docker-compose up --build  # Rebuild and reinitialize
```

Everything will be recreated from scratch automatically.
